from shiny import App, ui, render, reactive
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# Load world map data
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# List of all countries
all_countries = sorted(world['name'].tolist())

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select(
                "country",
                "Select countries you've visited:",
                choices=all_countries,
                multiple=True,
                selectize=True
            ),
            ui.output_text("selected_countries"),
        ),
        ui.output_plot("world_map")
    )
)

def server(input, output, session):
    @reactive.Calc
    def visited_countries():
        return input.country()

    @output
    @render.text
    def selected_countries():
        countries = visited_countries()
        if countries:
            return f"You've visited {len(countries)} countries: {', '.join(countries)}"
        else:
            return "You haven't selected any countries yet."

    @output
    @render.plot
    def world_map():
        visited = visited_countries()
        
        # Create a copy of the world dataframe
        world_copy = world.copy()
        
        # Create a new column for coloring
        world_copy['visited'] = world_copy['name'].isin(visited)
        
        # Set up the plot
        fig, ax = plt.subplots(figsize=(15, 10))
        
        # Create a custom colormap
        colors = ['#d3d3d3', '#66c2a5']  # Light gray for unvisited, teal for visited
        cmap = ListedColormap(colors)
        
        # Plot the world map
        world_copy.plot(column='visited', ax=ax, cmap=cmap, legend=False,
                        missing_kwds={'color': 'lightgrey'})
        
        # Create custom legend
        legend_elements = [Patch(facecolor='#d3d3d3', edgecolor='black', label='Not Visited'),
                           Patch(facecolor='#66c2a5', edgecolor='black', label='Visited')]
        ax.legend(handles=legend_elements, loc='lower left', title='Status')
        
        # Remove axis
        ax.axis('off')
        
        # Set title
        plt.title("Countries Visited", fontsize=16)
        
        return fig

app = App(app_ui, server)
