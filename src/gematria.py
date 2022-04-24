

# prepare the values dictionary
chars = "אבגדהוזחטיכלמנסעפצקרשת"
val = {chars[v]:v+1 for v in range(10)}
val.update({chars[v]:(v-8)*10 for v in range(10,19)})
val.update({chars[v]:(v-17)*100 for v in range(19,22)})
ends = ("מנצפכ", "םןץףך")
val.update({e:val[v] for v,e in zip(ends[0], ends[1])})

def gematria(word : str):
    """
    Convert a word to it's numeric value
    Support using first letter for thousands

    input : a hebrew word
    output : numerical value

    Examples :
        gematria("שלום")
            376
        gematria("שלום רב שובך ציפורה")
            1297
        gematria("ה'תשפב")
            5782
        gematria("גימטריה") == gematria("ערבה")
            True
    """
    thousands = 0
    if word[1] in "-'`":
        thousands = val.get(word[0],0)*1000
        word=word[2:]
    return thousands + sum([val.get(c,0) for c in word])