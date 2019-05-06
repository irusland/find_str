import grapher
from chronograph import Chronograph as Chrono
from memograph import Memograph as Memo
import finder
from textgen import Textgen
import statistics
import PyPDF2
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from textwrap import wrap


def get_time(points):
    res = []
    for t in points:
        for _, _, time in t:
            res.append(time)
    return min(res), float(statistics.median(res)), max(res)


def get_timemory(alg):
    t_best, p_best = Textgen('text.txt').generate_for(alg, best=True)
    t_worst, p_worst = Textgen('text.txt').generate_for(alg,
                                                        best=False)
    if alg in [finder.Linear, finder.Quad, finder.RabinKarph]:
        time_best, _ = Chrono(finder.Hash, alg).measure_accurate(
            t_best, p_best)
        mem_best = Memo(finder.Hash, alg).measure(t_best, p_best)

        time_worst, _ = Chrono(finder.Hash, alg).measure_accurate(
            t_worst, p_worst)
        mem_worst = Memo(finder.Hash, alg).measure(t_worst, p_worst)
    else:
        time_best, _ = Chrono(alg).measure_accurate(t_best, p_best)
        mem_best = Memo(alg).measure(t_best, p_best)
        time_worst, _ = Chrono(alg).measure_accurate(t_worst, p_worst)
        mem_worst = Memo(alg).measure(t_worst, p_worst)

    return time_best, mem_best, time_worst, mem_worst


def main():
    goal = 'This different substring search algorithms ' \
           'testing shows dependencies of a string ' \
           'preprocessing and other methods of search optimizing'

    specs = 'Processor: 3.4GHz Inter Core i5 \n' \
            'Memory: 8 GB 1600 MHz DDR3 \n' \
            'System: osx'

    results_explanation = {
        finder.BruteForce: 'Brute Force is pretty stable alghorithm, '
                           'works every time with O(n^2) asymptotic',

        finder.Linear: 'Hashes have a collision aspect that\'s why we '
                       'can see an abrupt behavior change and time growth'
                       'on a bad substring',

        finder.Quad: 'Hashes have a collision aspect that\'s why we '
                     'can see an abrupt behavior change and time growth'
                     'on a bad substring',

        finder.RabinKarph: 'Hashes have a collision aspect that\'s why we '
                           'can see an abrupt behavior change and time growth'
                           'on a bad substring',

        finder.Automate: 'Automate has a preprocessing aspect that\'s '
                         'why we can see time growth',

        finder.BoyerMoore: 'Boyer Moore algorithm works perfectly with '
                           'prepared pattern on every text but as we can see '
                           'there is recounting shift tables time delay',

        finder.KMP: 'KMP works fine on average string its pretty '
                    'stable',

        finder.SuffixArray: 'Suffix Array has a text preprocessing that '
                            'allows to work fast with O(n*log(n)) asymptotic '
                            'on every pattern'
    }
    algorithms = [
        (finder.BruteForce, 0),
        (finder.Linear, 1),
        (finder.Quad, 2),
        (finder.RabinKarph, 3),
        (finder.Automate, 4),
        (finder.BoyerMoore, 5),
        (finder.KMP, 6),
        (finder.SuffixArray, 7)
    ]

    grapher.build_graph()

    packet1 = io.BytesIO()
    can = canvas.Canvas(packet1, pagesize=letter)
    textobject = can.beginText()
    textobject.setTextOrigin(30, 470)

    textobject.setFont('Courier-Bold', 12)
    textobject.textLines("\n".join(wrap(goal, 79)))
    textobject.textLines('\n')
    textobject.setFont('Courier', 12)

    textobject.setFillColor(colors.blue)
    textobject.textLines(specs)
    textobject.textLines('\n')
    textobject.setFillColor(colors.black)

    textobject.textLines("\n".join(wrap(goal, 79)))

    can.drawText(textobject)
    can.save()

    output = PyPDF2.PdfFileWriter()
    pdf1 = PyPDF2.PdfFileReader(packet1)
    output.addPage(pdf1.getPage(0))

    for alg, page in algorithms:
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        textobject = can.beginText()
        textobject.setTextOrigin(30, 730)
        textobject.setFont('Courier-Bold', 12)
        textobject.textLines("\n".join(wrap(str(alg.__doc__), 79)))
        textobject.setFillColor(colors.red)
        textobject.textLines("\n".join(wrap(results_explanation[alg], 79)))
        textobject.textLines('\n')

        textobject.setFillColor(colors.darkgreen)
        time_best, mem_best, time_worst, mem_worst = get_timemory(alg)
        t_best, p_best = Textgen('text.txt').generate_for(alg, best=True)
        textobject.textLine(f'text    \'{t_best}')
        textobject.textLine(f'pattern \'{p_best}')
        textobject.textLines(f'Best case:\n{time_best} S\n{mem_best} B')

        textobject.setFillColor(colors.darkred)
        textobject.textLines('\n')
        t_worst, p_worst = Textgen('text.txt').generate_for(alg, best=False)
        textobject.textLine(f'text    \'{t_worst}')
        textobject.textLine(f'pattern \'{p_worst}')
        textobject.textLines(f'Worst case:\n{time_worst} S\n{mem_worst} B')

        can.drawText(textobject)
        can.save()

        pdf = PyPDF2.PdfFileReader(packet)
        graphs = PyPDF2.PdfFileReader(open('graphs.pdf', 'rb'))
        graph = graphs.getPage(page)
        page = pdf.getPage(0)
        page.mergePage(graph)
        output.addPage(page)

    output_stream = open("report.pdf", "wb")
    output.write(output_stream)
    output_stream.close()

    sizes = [
        # (100000, 0),
        # (100, 10),
        # (1000, 100),
        # (10000, 1000),
        # (100000, 100),
        # (1000000, 100),
    ]

    for text_size, pattern_size in sizes:
        text, pattern = Textgen('text.txt').generate(text_size)
        print(f'Generated: Text Length = {text_size}, '
              f'Pattern Size = {pattern_size}')
        results = [
            ('Brute Force',
             Chrono(finder.BruteForce).measure_accurate(text, pattern),
             Memo(finder.BruteForce).measure(text, pattern)),
            ('Hash Linear',
             Chrono(finder.Hash,
                    finder.Linear).measure_accurate(text, pattern),
             Memo(finder.Hash, finder.Linear).measure(text, pattern)),
            ('Hash Quad',
             Chrono(finder.Hash,
                    finder.Quad).measure_accurate(text, pattern),
             Memo(finder.Hash, finder.Quad).measure(text, pattern)),
            ('Hash RK',
             Chrono(finder.Hash,
                    finder.RabinKarph).measure_accurate(text, pattern),
             Memo(finder.Hash, finder.RabinKarph).measure(text, pattern)),
            ('Automate',
             Chrono(finder.Automate).measure_accurate(text, pattern),
             Memo(finder.Automate).measure(text, pattern)),
            ('Boyer Moore',
             Chrono(finder.BoyerMoore).measure_accurate(text, pattern),
             Memo(finder.BoyerMoore).measure(text, pattern)),
            ('KMP',
             Chrono(finder.KMP).measure_accurate(text, pattern),
             Memo(finder.KMP).measure(text, pattern)),
            ('Suffix Array',
             Chrono(finder.SuffixArray).measure_accurate(text, pattern),
             Memo(finder.SuffixArray).measure(text, pattern)),
        ]
        results = sorted(results, key=lambda _: _[1])
        for name, time_offset, memory in results:
            print(f'{name}\n\t%.6f S \n\t{memory} B' % time_offset[0])
        print(f'Best: {results[0]}')
        print(f'Worst: {results[-1]}')


if __name__ == '__main__':
    main()
