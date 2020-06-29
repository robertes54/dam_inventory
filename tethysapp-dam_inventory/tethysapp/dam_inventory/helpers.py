from plotly import graph_objs as go
from tethys_gizmos.gizmo_options import PlotlyView

from .app import DamInventory as app
from .model import Hydrograph


def create_hydrograph(hydrograph_id, height='520px', width='100%'):
    """
    Generates a plotly view of a hydrograph.
    """
    # Get objects from database
    Session = app.get_persistent_store_database('primary_db', as_sessionmaker=True)
    session = Session()
    hydrograph = session.query(Hydrograph).get(int(hydrograph_id))
    dam = hydrograph.dam
    time = []
    flow = []
    for hydro_point in hydrograph.points:
        time.append(hydro_point.time)
        flow.append(hydro_point.flow)

    # Build up Plotly plot
    hydrograph_go = go.Scatter(
        x=time,
        y=flow,
        name='Hydrograph for {0}'.format(dam.name),
        line={'color': '#0080ff', 'width': 4, 'shape': 'spline'},
    )
    data = [hydrograph_go]
    layout = {
        'title': 'Hydrograph for {0}'.format(dam.name),
        'xaxis': {'title': 'Time (hr)'},
        'yaxis': {'title': 'Flow (cfs)'},
    }
    figure = {'data': data, 'layout': layout}
    hydrograph_plot = PlotlyView(figure, height=height, width=width)
    session.close()
    return hydrograph_plot