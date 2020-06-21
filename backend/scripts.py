from reportlab.platypus import PageBreak, PageTemplate, BaseDocTemplate, Paragraph, NextPageTemplate, TableStyle, Image, Spacer
from reportlab.platypus.tables import Table
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.frames import Frame
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from django.db import models
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.lib.colors import Color, black
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import os
# from reportlab.pdfgen import canvas
import datetime

from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
registerFont(TTFont('Arial', 'ARIAL.ttf'))  # register arial fonts
registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))


# file location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(BASE_DIR, 'static\\images\\logo.jpg')
SKF = os.path.join(BASE_DIR, 'static\\images\\skf.jpg')
# datetime constants
MONTHS = (
    'enero',
    'febrero',
    'marzo',
    'abril',
    'mayo',
    'junio',
    'julio',
    'agosto',
    'septiembre',
    'octubre',
    'noviembre',
    'diciembre'
)
NOW = datetime.dateime.now()
CURRENT_YEAR = NOW.year
CURRENT_MONTH = NOW.month
CURRENT_DAY = NOW.day
# constants for footer
ADDRESS = 'Calle 9A  No. 54 - 129 Guayabal'
PHONE = 'PBX: (4) 362 00 62'
CELPHONE = 'Cel. 312 296 84 50'
WHATSAPP = 'WhatsApp 301  249 92 84'
WEBSITE = 'www.vibromontajes.com'
EMAIL = 'servicios@vibromontajes.com'
FOOTER_CITY = 'Medellín, Colombia'
# constants for colors
HEADER_FOOTER_GREEN = Color(red=0, green=(102/255), blue=0)
COMPANY_HEADER_BLUE = Color(red=(82/255), green=(139/255), blue=(166/255))
TABLE_BLUE = Color(red=(141/255), green=(179/255), blue=(226/255))
FOOTER_BLUE = Color(red=(84/255), green=(141/255), blue=(212/255))
# constants for paragraph styles
STANDARD = ParagraphStyle(
    name='standard', fontName='Arial', fontSize=10)
STANDARD_CENTER = ParagraphStyle(
    name='standard_center', fontName='Arial', fontSize=10, alignment=1)
STANDARD_HEADER = ParagraphStyle(
    name='standard_header', fontName='Arial', fontSize=10, alignment=2)
STANDARD_JUSTIFIED = ParagraphStyle(
    name='standard_justified', fontName='Arial', fontSize=10, alignment=4)
BLACK_BOLD = ParagraphStyle(
    name='black_bold', fontName='Arial-Bold', fontSize=10)
BLACK_BOLD_CENTER = ParagraphStyle(
    name='black_bold_center', fontName='Arial-Bold', fontSize=10, alignment=1)
BLUE_HEADER = ParagraphStyle(name='blue_hf', fontName='Arial-Bold', fontSize=10,
                             textColor=COMPANY_HEADER_BLUE, alignment=2)
BLUE_FOOTER = ParagraphStyle(name='blue_hf', fontName='Arial-Bold', fontSize=10,
                             textColor=FOOTER_BLUE, alignment=1)
BLACK_SMALL = ParagraphStyle(
    name='black_small', fontName='Arial', fontSize=7, alignment=1)
GREEN_SMALL = ParagraphStyle(
    name='green_small', fontName='Arial', fontSize=7, textColor=HEADER_FOOTER_GREEN, alignment=1)
# footer paragraph lines
LINE_ONE = Paragraph('_' * 80, style=BLUE_FOOTER)
LINE_TWO = Paragraph(
    f'{ADDRESS} {PHONE} {CELPHONE} {WHATSAPP}', style=BLACK_SMALL)
LINE_THREE = Paragraph(
    text=f'{WEBSITE} E-mail: <a href="mailto:{EMAIL}"><font color="blue">{EMAIL}</font></a> {FOOTER_CITY}', style=GREEN_SMALL)
# Frames used for templates
STANDARD_FRAME = Frame(1.6*cm, 2*cm, 18*cm, 26*cm,
                       id='standard')
MACHINE_FRAME = Frame(1.6*cm, 2*cm, 18*cm, 23*cm,
                      id='big_header')


class Report(BaseDocTemplate):

    """
    Create dynamic reports.
    """

    def __init__(self, filename, querysets, company, date, **kwargs):
        super().__init__(filename, **kwargs)
        self.filename = filename
        self.querysets = querysets  # model objects to populate pdf
        self.company = company
        self.date = date
        self.toc = TableOfContents()  # table of contents object
        self.story = []
        self.width = 18 * cm
        self.leftMargin = 1.6 * cm
        self.bottomMargin = 2 * cm
        self.templates = [
            PageTemplate(id='measurement',
                         frames=[MACHINE_FRAME],
                         onPage=self._header_one,
                         onPageEnd=self._footer),
            PageTemplate(id='measurement_two',
                         frames=[STANDARD_FRAME],
                         onPage=self._header_two,
                         onPageEnd=self._footer),
            PageTemplate(id='normal', frames=[
                         STANDARD_FRAME], onPage=self._header_two),
        ]
        self.addPageTemplates(self.templates)

    # finished

    def _create_header_table(self):
        """
        create table to manage
        elements in custom header.
        """

        logo = Image(LOGO, width=8.65 * cm, height=2.51 * cm)
        skf = Image(SKF, width=1.76 * cm, height=0.47 * cm)
        skf_text = Paragraph('Con tecnología', style=GREEN_SMALL)
        report_date = Paragraph(self.date.upper(), style=STANDARD_HEADER)
        company = Paragraph(self.company.upper(), style=BLUE_HEADER)
        data = [[logo, skf_text, report_date], ['', skf, company]]
        styles = [
            # align first column to the left horizontally
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            # align first column to the middle vertically
            ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
            # align 2nd column horizontally to center
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            # align first row in first column to the bottom vertically
            ('VALIGN', (1, 0), (1, 0), 'BOTTOM'),
            # align second row in first column to the top vertically
            ('VALIGN', (1, -1), (1, -1), 'TOP'),
            # align 3rd column vertically to center
            ('VALIGN', (2, 0), (2, -1), 'MIDDLE'),
            # align 3rd column horizontally to left
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            # merge first column
            ('SPAN', (0, 0), (0, -1)),
        ]
        table = Table(data, colWidths=[
                      9 * cm, 2.5 * cm, 6.5 * cm], rowHeights=[1.26 * cm, 1.26 * cm])
        table.setStyle(TableStyle(styles))
        return table

    @staticmethod
    def _create_footer_table():
        """
        create table to manage
        elements in footer.
        """

        data = [[LINE_ONE], [LINE_TWO], [LINE_THREE]]
        styles = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]
        table = Table(data, colWidths=[18 * cm],
                      rowHeights=[0.5 * cm, 0.4 * cm, 0.4 * cm])
        table.setStyle(TableStyle(styles))
        return table

    @staticmethod
    def _create_analysis_table(analysis, recomendation):
        """
        create table of analysis.
        """

        header_one = Paragraph(
            'ANÁLISIS DE VIBRACIÓN', style=STANDARD_CENTER)
        header_two = Paragraph(
            'CORRECTIVOS Y/O RECOMENDACIONES', style=STANDARD_CENTER)
        analysis = Paragraph(analysis, style=STANDARD)
        recomendation = Paragraph(recomendation, style=STANDARD)

        data = [[header_one], [analysis],
                [header_two], [recomendation]]
        styles = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]
        table = Table(data, colWidths=[18 * cm])
        table.setStyle(TableStyle(styles))
        return table

    @ staticmethod
    def graph_table(title, graph):
        """
        create a table containing
        an especified graphic.
        """

        title = Paragraph(title, style=STANDARD_CENTER)
        graph = Image(graph, width=17 * cm, height=6 * cm)
        data = [[title], [graph]]
        styles = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 0), (0, 0), TABLE_BLUE),
            ('GRID', (0, 0), (-1, -1), 0.25, black)
        ]
        table = Table(data, colWidths=[18 * cm], rowHeights=[0.5 * cm, 7 * cm])
        table.setStyle(TableStyle(styles))
        return table

    def _header_one(self, canvas, doc):
        """
        method to be passed to PageTemplate
        objects on onPage keyword argument 
        to generate headers of measurements.
        """

        canvas.saveState()
        page = Paragraph(str(doc.page), style=BLACK_SMALL)
        w, h = page.wrap(self.width, 1 * cm)
        page.drawOn(canvas, self.leftMargin +
                    ((self.width - w) / 2), (29 * cm) - h)
        table = self._create_header_table()
        _, ht = table.wrap(self.width, 3 * cm)
        table.drawOn(canvas, self.leftMargin, 28 * cm - ht)
        canvas.restoreState()

    def _header_two(self, canvas, doc):
        """
        method to be passed to PageTemplate
        objects on onPage keyword argument 
        to generate basic headers.
        """

        canvas.saveState()
        page = Paragraph(str(doc.page), style=BLACK_SMALL)
        w, h = page.wrap(self.width, 1 * cm)
        page.drawOn(canvas, self.leftMargin +
                    ((self.width - w) / 2), (29 * cm) - h)
        canvas.restoreState()

    def _footer(self, canvas, doc):
        """
        method to be passed to PageTemplate
        objects on onPageEnd keyword argument
        to generate footers.
        """

        canvas.saveState()
        table = self._create_footer_table()
        _, h = table.wrap(self.width, self.bottomMargin)
        table.drawOn(canvas, self.leftMargin, (2 * cm - h) / 2)
        canvas.restoreState()

    # TODO

    def build_doc(self):
        """
        build document.
        """
        self.addPageTemplates(self.templates)
        self.story += [Paragraph(
            'CORRECTIVOS Y/O RECOMENDACIONES', style=STANDARD_CENTER), NextPageTemplate("measurement"), PageBreak(), Paragraph(
            'CORRECTIVOS Y/O RECOMENDACIONES', style=STANDARD_CENTER), self._create_analysis_table('aaaaaaa<br/>asdasdasdasd ' * 10, 'asdasdasdadds ' * 90)]
        self.write_pdf()

        self.multiBuild(self.story)

    def create_letter_one(self):
        pass

    def create_letter_two(self):
        pass

    def write_pdf(self):
        """
        generate document flowables
        according to queryset.
        """
        # TODO
        return self

    @staticmethod
    def pictures_table(diagram_img, machine_img):
        """
        create a table containing the 
        diagram image and the machine image.
        """

        diagram_img = Image(diagram_img)
        machine_img = Image(machine_img)
        diagram = Paragraph('DIAGRAMA ESQUEMATICO', style=STANDARD)
        machine = Paragraph('IMAGEN MAQUINA', style=STANDARD)
        data = [[diagram, machine], [diagram_img, machine_img]]
        styles = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.25, black),
            ('BACKGROUND', (0, 0), (1, 0), TABLE_BLUE)
        ]
        table = Table(data, colWidths=[
                      9 * cm, 9 * cm], rowHeights=[0.5 * cm, 6 * cm])
        table.setStyle(TableStyle(styles))
        return table

    def machine_specifications_table(self):
        """
        create table detailing especifications 
        of each machine and their current severity.
        """

        data = None
        styles = None
        table = Table(data, colWidths=[18 * cm], rowHeights=[0.5 * cm, 7 * cm])
        table.setStyle(TableStyle(styles))
        return table

    def afterFlowable(self, flowable):
        "Registers TOC entries."

        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                self.notify('TOCEntry', (0, text, self.page))
            if style == 'Heading2':
                self.notify('TOCEntry', (1, text, self.page))

    def create_table(self, engine_name, previous_date, current_date, data):
        """
        create table graph for word.
        """

        fig, ax = plt.subplots()  # create axes and figure objects
        columns = [
            '$\\bfNombre$ $\\bfde$ $\\bfPUNTO$',
            '$\\bfUnidades$',
            f'$\\bfValor$ $\\bfanterior$\n$\\bf{previous_date}$',
            f'$\\bfÚlt.$ $\\bfvalor$\n$\\bf{current_date}$',
            '$\\bf\%$ $\\bfcambio$'
        ]
        fig.patch.set_visible(False)  # remove graph plot from figure
        colors = []  # 2d list containing all lists of colors for each row
        # list comprehension to define blue color of first rows
        col_colors = ['#8DB3E2' for _ in range(len(columns))]
        col_widths = [0.3, 0.2, 0.25, 0.2, 0.2]
        for rows in data:  # define color of rows in table
            row_colors = []  # 2d list containing all colors for all rows
            # format first element in a row to be bold
            rows[0] = f'$\\bf{rows[0]}$'
            for _ in rows:  # iterate through every cell in each row
                if data.index(rows) % 2 == 0:  # if index is even set color to white
                    row_colors.append('#FFFFFF')
                else:  # if index is odd set color to blueish
                    row_colors.append('#DCE6F1')
            colors.append(row_colors)  # append list to colors list
        ax.axis('off')
        ax.axis('tight')
        # define table title and place 1.1 above table
        plt.title(engine_name, y=1.1)
        table = ax.table(cellText=data, cellColours=colors, colWidths=col_widths, colColours=col_colors,
                         colLabels=columns, loc='center', cellLoc='center')  # define table object
        table.set_fontsize(10)  # set font size for table
        table.scale(0.8, 1)  # stretch table horizontally
        cellDict = table.get_celld()  # dict of all cells in table
        for i in range(0, len(columns)):  # go through all cells in first column
            # change height to be able to adjust text
            cellDict[(0, i)].set_height(.1)
        fig.tight_layout()  # set tight_layout to adjust objects in figure
    #     plt.savefig('tabla', bbox_inches="tight", transparent=True, dpi=300)  # save figure as tabla.png along with other properties

    def create_graph(self, g, title, save):
        """
        create chart graph of tendency
        values for vel or acc.
        """

        labels = g['name'].unique()
        # obtain the unique values for the 'name' column of the dataframe
        # if name's 2nd character is not numeric and 3rd character is equal to V unit is mm/s, if A it will b g - RMS
        if not labels[0][1].isnumeric():
            if labels[0][2] == 'V':
                units = 'mm/s - Pico'
            else:
                units = 'g - RMS'
        else:
            # if name's 2nd character is numeric and 4th character is equal to V unit is mm/s, if A it will b g - RMS
            if labels[0][3] == 'V':
                units = 'mm/s - Pico'
            else:
                units = 'g - RMS'
        # colors for all 12 possible lines in a plot
        my_colors = [
            'b',
            'r',
            '#006600',
            '#ff66cc',
            '#00ff00',
            '#ffff00',
            '#660066',
            '#00ffff',
            '#F39C12',
            '#148F77',
            '#C0392B',
            '#0E6251'
        ]
        index = 0
        # create figure and axes objects
        fig, ax = plt.subplots(figsize=(17, 6))
        for label in labels:  # plot a line for every label
            # obtain the dates for every label in the dataframe
            dates = [datetime.datetime(int(f[:4]), int(f[4:6]), int(
                f[6:8])) for f in g.loc[g['name'] == label]['date'].values]
            # obtain the data for every label in the dataframe
            data = [float(v)
                    for v in g.loc[g['name'] == label]['global'].values]
            ax.plot_date(dates, data, linestyle='solid', label=label,
                         color=my_colors[index], marker='.')  # plot label
            index += 1
        plt.style.use('seaborn-ticks')  # define style for graph
        date_format = mpl_dates.DateFormatter(
            '%d/%m/%Y')  # define date format for x axis
        ax.xaxis.set_major_formatter(date_format)  # set format to axis
        # set title accorind to title and last label variables
        ax.set_title(f'Tendencia\n{title}\\{labels[-1]}, Canal X')
        # set x axis label and separate from axis
        ax.set_xlabel('Fecha', labelpad=5)
        ax.set_ylabel(units)  # set y axis label
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True,
                  shadow=True, ncol=1)  # set legend location and other parameters
        plt.grid(True)  # add grid to plot
        plt.tight_layout()  # adjust plot params
        plt.savefig(save, bbox_inches="tight", transparent=True,
                    dpi=300)  # save figure to be placed in document


Report('test.pdf', 'hi', 'company', 'date').build_doc()
