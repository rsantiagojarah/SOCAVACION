"""Ingreso reducido para sección rectangular y aproximación uniforme confirmadas."""
import typer
from socavacion.domain.enums import FormaEstribo, FormaPilar
from socavacion.domain.models import Proyecto, Estribo, Pilar, CondicionHidraulica, DatosGeotecnia, ClasificacionCauce
from socavacion.input.prompts import numero, texto, opcion


def hidraulica_rectangular(*, Q, B, h, dm, z, beta, luz, fuentes, L=None):
    """Derivación registrada; Qe se obtiene de una franja uniforme, nunca de Q1 entero."""
    if min(Q,B,h,dm,z,beta,luz)<=0 or (L is not None and not 0<L<=B):
        raise ValueError('La sección y la franja obstruida deben tener dimensiones positivas y L<=B.')
    V=Q/(B*h)
    datos=dict(y1=h,V1=V,W1=B,W2=B,y0=h,Q_ll=Q,B_ll=B,h_m_ll=h,h_local=h,
               Dm_mm=dm,exponente_x=z,beta=beta,luz_libre=luz,V_mu=V,phi=1.0,
               fuentes=dict(fuentes))
    if L is not None:
        datos.update(L_obstruida=L,Ae=L*h,Qe=Q*L/B)
    hid=CondicionHidraulica(**datos)
    hid.resolver_q(Q)
    return hid


def ejecutar_basico(base=None, salida=None):
    prueba=bool(base and base.datos_prueba)
    muestra=base.estribo_izquierdo if base else None
    hidbase=muestra.q100 if muestra else None
    typer.echo('\nINGRESO BÁSICO: sólo socavación, sección rectangular y lecho granular homogéneo.\n'
               'Se calcularán V=Q/(B*h), alpha, mu por Tabla 13 y factores locales por forma/ángulo.\n'
               'phi=1 y K4=1: sin reducción por sedimentos/armadura. No se evalúan cimentaciones.\n'
               'Use --avanzado para geometrías, velocidades o materiales diferentes por apoyo.')
    nombre=texto('Nombre del proyecto',default=base.nombre if base else '')
    if not typer.confirm('¿Confirma sección rectangular, flujo libre y distribución uniforme aplicable también a los apoyos?',default=prueba):
        raise ValueError('El ingreso básico no aplica. Reinicie con --avanzado y proporcione hidráulica por apoyo.')
    q100=numero('Q100 (m³/s)',default=base.Q100 if base else None,positivo=True)
    q500=numero('Q500 (m³/s)',default=base.Q500 if base else None,positivo=True,minimo=q100)
    qot=numero('Q desbordamiento (m³/s)',opcional=True,positivo=True)
    tot=numero('T desbordamiento (años)',positivo=True,maximo=500) if qot is not None else None
    B=numero('Ancho hidráulico B de la sección rectangular (m)',default=hidbase.B_ll if hidbase else None,positivo=True)
    luz=numero('Luz libre mínima entre apoyos (m), para tabla mu',default=hidbase.luz_libre if hidbase else None,minimo=10,maximo=200)
    dm=numero('Dm característico del lecho (mm)',default=hidbase.Dm_mm if hidbase else None,positivo=True)
    d50=numero('D50 (mm), distinto de Dm; diagnóstico y pilares',default=muestra.D50_mm if muestra else None,positivo=True)
    typer.echo('beta y z NO se asignan con una tabla MTC verificada en este motor; los valores mostrados son supuestos del ejemplo.')
    z=numero('z granular (una vez para el material)',default=hidbase.exponente_x if hidbase else None,positivo=True)
    lp=numero('Degradación de largo plazo (m)',default=base.cauce.y_sg_lp if base else None)
    eventos=[('q100',q100,muestra.q100 if muestra else None),('q500',q500,muestra.q500 if muestra else None)]
    if qot is not None:
        eventos.append(('qot',qot,None))
    hidraulicas=[]
    for etiqueta,Q,previo in eventos:
        h=numero(f'{etiqueta}: tirante h de la sección (m)',default=previo.y1 if previo else None,positivo=True)
        beta=numero(f'{etiqueta}: beta sustentado (no automático)',default=previo.beta if previo else None,positivo=True)
        hidraulicas.append((etiqueta,Q,h,beta))
        typer.echo(f'  V calculada = {Q/(B*h):.4f} m/s; h_local = hm = {h:g} m.')
    forma=opcion('Forma de ambos estribos',[f.value for f in FormaEstribo],default=muestra.forma.value if muestra else 'muro_vertical')
    theta=numero('Ángulo de ambos estribos (90 = normal)',default=muestra.angulo_ataque if muestra else 90,positivo=True,maximo=180)
    apoyos=[]
    for lado in ('izquierdo','derecho'):
        previo=getattr(base,'estribo_'+lado) if base else None
        L=numero(f'Estribo {lado}: longitud obstruida L (m)',default=previo.L_prima if previo else None,positivo=True,maximo=B)
        Z=numero(f'Estribo {lado}: cota lecho (m, datum común)',default=previo.Z_lecho if previo else None)
        apoyos.append((lado,L,Z))
    if sum(a[1] for a in apoyos)>B:
        raise ValueError('Las franjas obstruidas de ambos estribos se superponen (L_izq+L_der>B). Revise geometría o use --avanzado.')
    n=numero('Número de pilares',default=len(base.pilares) if base else 0,minimo=0,entero=True)
    pilares=[]
    for i in range(n):
        previo=base.pilares[i] if base and i<len(base.pilares) else None
        a=numero(f'P{i+1}: ancho real a (m)',default=previo.ancho_a if previo else None,positivo=True)
        l=numero(f'P{i+1}: longitud real l (m)',default=previo.longitud_l if previo else None,minimo=a)
        ang=numero(f'P{i+1}: ángulo respecto al flujo (grados)',default=previo.angulo_ataque if previo else 0,minimo=0,maximo=180)
        f=opcion(f'P{i+1}: forma',[f.value for f in FormaPilar],default=previo.forma.value if previo else 'circular')
        Z=numero(f'P{i+1}: cota lecho (m)',default=previo.Z_lecho if previo else None)
        lecho=opcion(f'P{i+1}: forma del lecho (Tabla 22)', ['plano','dunas_pequenas','dunas_medianas','dunas_grandes'],default='plano')
        k3={'plano':1.1,'dunas_pequenas':1.1,'dunas_medianas':1.2,'dunas_grandes':1.3}[lecho]
        pilares.append(dict(nombre=f'P{i+1}',ancho_a=a,longitud_l=l,angulo_ataque=ang,forma=f,Z_lecho=Z,K3=k3,K4=1,D50_mm=d50))
    fuente=texto('Fuente común de hidrología, geometría y suelo (documento/secciones; opcional en preliminar)',
                 default='EX: ejemplo sintético de software, sin mediciones de campo' if prueba else '',requerido=False)
    coef=texto('Fuente de beta y z (documento/tabla/página; opcional en preliminar)',
               default='EX-06: coeficientes de ensayo, no tabla normativa validada' if prueba else '',requerido=False)
    fp={k:fuente for k in ('hidrologia','topografia','largo_plazo') if fuente}
    fh={k:fuente for k in ('hidraulica','geometria','granulometria','luz_libre','pilar') if fuente}
    fh.update({k:coef for k in ('beta','exponente_x') if coef})
    fh.update(phi='phi=1, sin reducción por transporte; supuesto conservador explícito',
              cierre_alpha='Sección rectangular confirmada: alpha=Q/(B*h^(5/3)), V=Q/(B*h)',
              local='Flujo uniforme confirmado: Ae=L*h, Qe=Q*L/B; coeficientes de forma/ángulo HHD Tab.27/ec.93')
    def condiciones(L=None):
        return {e:hidraulica_rectangular(Q=Q,B=B,h=h,dm=dm,z=z,beta=b,luz=luz,fuentes=fh,L=L)
                for e,Q,h,b in hidraulicas}
    estribos=[Estribo(lado=lado,L_prima=L,Ae=0,Z_lecho=Z,D50_mm=d50,forma=forma,
                     angulo_ataque=theta,**condiciones(L)) for lado,L,Z in apoyos]
    proyecto=Proyecto(nombre=nombre,modo='preliminar',datos_prueba=prueba,Q100=q100,Q500=q500,Q_ot=qot,T_ot=tot,
        estribo_izquierdo=estribos[0],estribo_derecho=estribos[1],
        pilares=[Pilar(**p,**condiciones()) for p in pilares],
        cauce=ClasificacionCauce(tipo='degradacion' if lp>0 else 'agradacion' if lp<0 else 'estable',y_sg_lp=lp),
        geotecnia=DatosGeotecnia(evaluar=False,hay_estrato_competente=False),fuentes=fp,
        supuestos=['INGRESO BÁSICO: sección rectangular, material común homogéneo, flujo uniforme; validar antes de diseño.',
                   'V=Q/(B*h); h_local=hm=h; Ae=L*h; Qe=Q*L/B por estribo; y0/W2 representan la sección idealizada.',
                   'phi=1 y K4=1 sin reducción; K3 por Tabla 22 (para dunas medianas se adopta extremo superior 1.2).',
                   'No se evaluó geotecnia ni se fijó cota de cimentación; Sf y velocidad de corte no se necesitan en estas fórmulas.'])
    if salida is None:
        destino=texto('Guardar entrada YAML (ruta; Enter para no guardar)',requerido=False)
        salida=destino or None
    if salida is not None:
        from socavacion.input.wizard import _guardar
        _guardar(proyecto,salida)
    return proyecto
