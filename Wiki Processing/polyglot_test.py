# -*- coding: utf-8 -*-
import polyglot

from polyglot.text import Text, Word, WordList
from polyglot.tag.base import TransferPOSTagger

from nltk.tokenize import ToktokTokenizer

import timeit


langs = ("en", "ar", "vi", "ja", "ko")

# print("initialising taggers")
# transfer_taggers = {l: TransferPOSTagger(l) for l in langs}
# print("initialised taggers")

# def get_pos_tags(raw_text, lang):
#     pg_text = Text(raw_text)
#     pg_text.pos_tagger = transfer_taggers[lang]
#     return pg_text.pos_tags





if __name__ == '__main__':


    raw_en = "The Portage to San Cristobal of A.H. is a 1981 literary and philosophical novella by George Steiner (pictured). The story is about Jewish Nazi hunters who find a fictional Adolf Hitler (A.H.) alive in the Amazon jungle thirty years after the end of World War II."

    raw_ar = 'سليمان خان الأول بن سليم خان الأول، هو عاشر السلاطين العثمانيين وخليفة المسلمين الثمانون، وثاني من حمل لقب "أمير المؤمنين" من آل عثمان. بلغت الدولة الإسلامية في عهده أقصى اتساع لها حتى أصبحت أقوى دولة في العالم في ذلك الوقت. وصاحب أطول فترة حكم من 6 نوفمبر 1520م حتى وفاته في 7 سبتمبر سنة 1566م خلفاً لأبيه السلطان سليم خان الأول وخلفه ابنه السلطان سليم الثاني.'

    raw_vi = "Kẽm là một nguyên tố kim loại chuyển tiếp, ký hiệu là Zn và có số nguyên tử là 30. Nó là nguyên tố đầu tiên trong nhóm 12 của bảng tuần hoàn các nguyên tố."

    raw_ja = "辞典等には以上のようにあるわけだが、これは大きく二分すると「自然言語」と「形式言語」とがあるうちの自然言語について述べている。しかし、1950年代以降の言語学などでは、定義中にも「記号体系」といった表現もあるように形式的な面やその扱い、言い換えると形式言語的な面も扱うようになっており、こんにちの言語学において形式体系と全く無関係な分野はそう多くはない。形式的な議論では、「その言語における文字の、その言語の文法に従った並び」の集合が「言語」である、といったように定義される。"

    raw_ko = """특히 국제 분쟁 조정을 위해 북한의 김일성, 아이티의 세드라스 장군, 팔레인스타인의
하마스, 보스니아의 세르비아계 정권 같이 미국 정부에 대해 협상을 거부하면서 사태의
위기를 초래한 인물 및 단체를 직접 만나 분쟁의 원인을 근본적으로 해결하기 위해 힘썼
다. 이 과정에서 미국 행정부와 갈등을 보이기도 했지만, 전직 대통령의 권한과 재야 유
명 인사들의 활약으로 해결해 나갔다."""

    t_en, t_ar, t_vi, t_ja, t_ko = Text(raw_en), Text(raw_ar), Text(raw_vi), Text(raw_ja), Text(raw_ko)

    print(t_en.words)
    print()
    print(t_ar.words)
    print()
    print(t_vi.words)
    print()
    print(t_ja.words)
    print()
    print(t_ko.words)

    print("\n")

    print("polyglot:")
    print(timeit.timeit("Text('辞典等には以上のようにあるわけだが、これは大きく二分すると「自然言語」と「形式言語」とがあるうちの自然言語について述べている。しかし、1950年代以降の言語学などでは、定義中にも「記号体系」といった表現もあるように形式的な面やその扱い、言い換えると形式言語的な面も扱うようになっており、こんにちの言語学において形式体系と全く無関係な分野はそう多くはない。形式的な議論では、「その言語における文字の、その言語の文法に従った並び」の集合が「言語」である、といったように定義される。').words",
                        number=10000,
                  setup = "from polyglot.text import Text; "))
    print()

    print("TokTok:")
    print(timeit.timeit("toktok.tokenize('辞典等には以上のようにあるわけだが、これは大きく二分すると「自然言語」と「形式言語」とがあるうちの自然言語について述べている。しかし、1950年代以降の言語学などでは、定義中にも「記号体系」といった表現もあるように形式的な面やその扱い、言い換えると形式言語的な面も扱うようになっており、こんにちの言語学において形式体系と全く無関係な分野はそう多くはない。形式的な議論では、「その言語における文字の、その言語の文法に従った並び」の集合が「言語」である、といったように定義される。')",
                        number=10000,
                        setup = "from nltk.tokenize import ToktokTokenizer; toktok = ToktokTokenizer()"))
    print("\n")


    # tt = ToktokTokenizer()
    #
    # tt.tokenize('Kẽm là một nguyên tố kim loại chuyển tiếp, ký hiệu là Zn và có số nguyên tử là 30. Nó là nguyên tố đầu tiên trong nhóm 12 của bảng tuần hoàn các nguyên tố.')


    # print(Text(raw_en.replace(" ", ""), hint_language_code="en").morphemes)
    #
    #
    # ws_en = map(lambda w: Word(w, language="en"), t_en.words)
    #
    # for w in ws_en:
    #     print(w, "\t", w.morphemes)



    print(t_en.transfer_pos_tags, "\n")
    print(t_ar.transfer_pos_tags, "\n")
    print(t_vi.transfer_pos_tags, "\n")
    print(t_ja.transfer_pos_tags, "\n")
    print(t_ko.transfer_pos_tags, "\n")



    # vi_pos_tags_single = []
    #
    # for w in Text(raw_vi).words:
    #     w_t = Text(w)
    #     w_t.pos_tagger = TransferPOSTagger("vi")
    #     vi_pos_tags_single.append(w_t.pos_tags[0])
    #
    #
    #
    #
    # for (w, t), (w2, t2) in zip(get_pos_tags(raw_vi, "vi"), vi_pos_tags_single):
    #     print(w, "\t", t, "\t", t2)

