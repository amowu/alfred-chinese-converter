# -*- coding: utf8 -*-
import alfred
import opencc


def process(query_str):
    """Entry Point"""
    if query_str is not None:
        results = alfred_items_for_value(query_str)
        xml = alfred.xml(results)  # compiles the XML answer
        alfred.write(xml)  # writes the XML back ti Alfred


def alfred_items_for_value(value):
    """
    Given a Chinese language string, return a list of alfred items for each of the results
    """
    index = 0
    results = []

    config_list = [
        ('t2s.json', u'繁體到簡體', 'SimplifiedChinese.png'),
        ('s2t.json', u'簡體到繁體', 'TraditionalChinese.png'),
        ('s2tw.json', u'簡體到臺灣正體', 'TW_taiwan.png'),
        ('tw2s.json', u'臺灣正體到簡體', 'CN_china.png'),
        ('s2hk.json', u'簡體到香港繁體', 'HK_hongKong.png'),
        ('hk2s.json', u'香港繁體（香港小學學習字詞表標準）到簡體', 'CN_china.png'),
        ('s2twp.json', u'簡體到繁體（臺灣正體標準）並轉換爲臺灣常用詞彙', 'TW_taiwan.png'),
    ]
    for config_file, description, icon in config_list:
        converter = opencc.OpenCC(
            config=config_file, opencc_path='/usr/local/bin/opencc')
        item_value = converter.convert(value)
        results.append(alfred.Item(
            title=item_value,
            subtitle=description,
            attributes={
                'uid': alfred.uid(index),
                'arg': item_value,
            },
            icon=icon,
        ))
        index += 1

    return results

if __name__ == '__main__':
    try:
        query_str = alfred.args()[0]
    except IndexError:
        query_str = None
    process(query_str)
