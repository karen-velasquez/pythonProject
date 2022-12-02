from kivymd.app import MDApp
from kivy.lang.builder import Builder

from kivymd_extensions.akivymd.uix.charts import AKBarChart

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
MDScreen:

    MDBoxLayout:
        orientation: 'vertical'

        ScrollView:

            MDBoxLayout:
                id: layout
                orientation: 'vertical'
                spacing: 20
                padding: 10
                adaptive_height: True


                AKBarChart:
                    size_hint_y: None
                    height: "280dp"
                    id: chart
                    labels: True
                    label_size: 15
                    bars_radius: 0

                    # Customize the colors

                    # bars colors
                    bars_color: get_color_from_hex("#4CD6D7")

                    # background color
                    bg_color: get_color_from_hex("#363E41")

                    # line color
                    lines_color: get_color_from_hex("#363E41")


'''


class BarChartApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        chart = self.root.ids.chart

        # setting the x values
        chart.x_values = list(range(4))

        # setting the y values
        chart.y_values = [30, 69, 75, 90]

        # adding x labels
        chart.x_labels = ['C', 'C++', 'Java', 'Python']


if __name__ == '__main__':
    BarChartApp().run()