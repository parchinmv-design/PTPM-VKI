"""
Генератор отчёта ЛР2 в формате .docx.
Создаёт минимальный валидный DOCX без внешних зависимостей.
"""

import zipfile
import os
from xml.sax.saxutils import escape


def create_docx(filename, paragraphs):
    """
    Создаёт .docx файл с плоским списком абзацев.
    Каждый элемент списка — кортеж (text, style), где style:
      'Title' — заголовок
      'Heading1' — заголовок раздела
      'Heading2' — подзаголовок
      'Normal' — обычный текст
      'ListItem' — пункт списка
    """
    styles_map = {
        'Title': 'Title',
        'Heading1': 'Heading1',
        'Heading2': 'Heading2',
        'Normal': 'Normal',
        'ListItem': 'ListItem',
    }

    body_parts = []
    for text, style in paragraphs:
        style_id = styles_map.get(style, 'Normal')
        body_parts.append(
            f'<w:p><w:pPr><w:pStyle w:val="{style_id}"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'
        )

    sect_pr = '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/></w:sectPr>'

    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:body>' + ''.join(body_parts) + sect_pr + '</w:body></w:document>'
    )

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '</Types>'
    )

    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '</Relationships>'
    )

    doc_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        '</Relationships>'
    )

    styles_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>'
        '<w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr>'
        '<w:rPr><w:b/><w:sz w:val="48"/></w:rPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
        '<w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>'
        '<w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
        '<w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr>'
        '<w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Normal"><w:name w:val="Normal"/>'
        '<w:pPr><w:spacing w:after="120"/></w:pPr>'
        '<w:rPr><w:sz w:val="24"/></w:rPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="ListItem"><w:name w:val="List Paragraph"/>'
        '<w:pPr><w:spacing w:after="60"/></w:pPr>'
        '<w:rPr><w:sz w:val="24"/></w:rPr></w:style>'
        '</w:styles>'
    )

    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', styles_xml)
        zf.writestr('word/_rels/document.xml.rels', doc_rels)


def main():
    report_path = os.path.join(os.path.dirname(__file__), 'Отчёт_ЛР2.docx')

    paragraphs = [
        ("Отчёт по лабораторной работе №2", 'Title'),
        ("Юнит-тестирование проектов и автоматизация проверок", 'Normal'),
        ("", 'Normal'),

        ("Пункт А: Общая статистика", 'Heading1'),
        ("", 'Normal'),
        ("Модуль my_project.py (код из ЛР1): написано 25 тестов, все проходят успешно.", 'Normal'),
        ("Модуль delivery_service.py (предоставленный код): написано 24 теста, из них 5 падают.", 'Normal'),
        ("Итого: 49 тестов, 44 проходят, 5 падают.", 'Normal'),
        ("", 'Normal'),

        ("Пункт Б: Упавшие тесты для delivery.py", 'Heading1'),
        ("", 'Normal'),
        ("Общее количество упавших тестов: 5.", 'Normal'),
        ("Все падения связаны с двумя багами в логике расчёта экспресс-доставки.", 'Normal'),
        ("", 'Normal'),

        ("Пункт В: Локализация аномалий", 'Heading1'),
        ("", 'Normal'),

        ("Баг 1: Экспресс-доставка снижает стоимость вместо повышения", 'Heading2'),
        ("", 'Normal'),
        ("Строка 36: total_cost *= 0.5", 'Normal'),
        ("Описание дефекта: при включённой экспресс-доставке итоговая стоимость умножается на 0.5, что снижает её вдвое. По бизнес-логике экспресс-доставка должна стоить дороже.", 'Normal'),
        ("Вариант исправления: total_cost *= 1.5", 'Normal'),
        ("", 'Normal'),

        ("Баг 2: Экспресс-доставка может дать нулевой срок доставки", 'Heading2'),
        ("", 'Normal'),
        ("Строка 44: days_needed = days_needed // 2", 'Normal'),
        ("Описание дефекта: для дистанций до 500 км days_needed = 1, и после деления на 2 без проверки минимума получается 0 дней. Доставка не может занять 0 дней.", 'Normal'),
        ("Вариант исправления: days_needed = max(1, days_needed // 2)", 'Normal'),
        ("", 'Normal'),

        ("Упавшие тесты:", 'Heading2'),
        ("", 'Normal'),
        ("1. test_express_increases_cost — строка 36.", 'ListItem'),
        ("2. test_express_with_light_package — строка 36.", 'ListItem'),
        ("3. test_express_with_fragile_package — строка 36.", 'ListItem'),
        ("4. test_express_delivery_date_short_distance — строка 44.", 'ListItem'),
        ("5. test_express_delivery_date_long_distance — строка 44.", 'ListItem'),
    ]

    create_docx(report_path, paragraphs)
    print(f"Отчёт создан: {report_path}")


if __name__ == '__main__':
    main()
