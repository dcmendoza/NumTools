from django.shortcuts import render
import Methods.utils.resources as rs
import Methods.utils.numerical_methods as nm
from .forms import FalsePositionForm

# Create your views here.
def false_position_view(request):
    context = {}
    if request.method == 'POST':
        form = FalsePositionForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            fun = form.cleaned_data['fun'].replace('^', '**').replace(' ', '')
            xi = form.cleaned_data['xi']
            xs = form.cleaned_data['xs']
            tol = form.cleaned_data['tol']
            niter = form.cleaned_data['niter']
            precision_type = form.cleaned_data['precision_type']
            precision_value = form.cleaned_data['precision_value']

            try:
                # Ejecutar el método de la falsa posición
                fm, error,xm_values, root, iterations = nm.falseposition_method(xi, xs, tol, niter, fun, rs.to_math)
                # Definir el tipo de error a mostrar en la tabla
                error_type = 'Relative Error' if precision_type == 'significant_figures' else 'Absolute Error'

                # Si se encuentra la raíz, ajustar con la precisión solicitada
                if root is not None:
                    if precision_type == 'significant_figures':
                        fm = [rs.round_to_significant_figures(f, precision_value) for f in fm]
                        root = rs.round_to_significant_figures(root, precision_value)
                        error = [rs.round_to_significant_figures(e, precision_value) for e in error]
                    elif precision_type == 'decimal_places':
                        fm = [round(f, precision_value) for f in fm]
                        root = round(root, precision_value)
                        error = [round(e, precision_value) for e in error]
                img_base64 = rs.generate_graph(xi, xs, fun, root)

                # Crear contexto con los resultados
                context = {
                    'form': form,
                    'fx': fun,
                    'msg': ['Cálculo completado'],
                    'graph': img_base64,
                    'table': [{'iteration': i, 'x_n': xm_values[i], 'fx_n': fm[i], 'error': error[i]} for i in range(iterations)],
                    'error_type': error_type,
                    'root': root,
                }
            except Exception as e:
                context['form'] = form
                context['msg'] = [f"Error: {str(e)}"]
        else:
            context['form'] = form
    else:
        context['form'] = FalsePositionForm()
    return render(request, 'falseposition.html', context)
