import math

def DotProd(x1, x2):
    sum = 0
    for i, j in zip(x1, x2):
        sum += i * j
    return sum

def ElemSubtract(x1, x2):
    diff = []
    for i, j in zip(x1, x2):
        diff.append(i - j)
    return diff

def ElemSquare(x1):
    squares = []
    for i in x1:
        squares.append(i ** 2)
    return squares

def getMySSE (x1, x2):
    diff = ElemSubtract(x1, x2)
    diff_square = ElemSquare(diff)
    diff_sum = sum(diff_square)
    return diff_sum

def sumOfHalfSlide (x1, x2, i, j):
    x1_slide = x1[0 : i]
    x2_slide = x2[j : len(x1)]
    diff_sum = getMySSE(x1_slide, x2_slide)/i
    return diff_sum

def SlidingWindow(x1, x2):
    stats = {}
    for i in range(1, len(x1)):
        j = len(x1) - i
        stats[i] = sumOfHalfSlide(x1, x2, i, j)
        stats[-j] = sumOfHalfSlide(x2, x1, i, j)
    diff_sum_inline = getMySSE(x1, x2)
    stats[0] = diff_sum_inline/len(x1)
    return stats

def CorrOfHalfSlide (x1, x2, i, j):
    x1_slide = x1[0 : i]
    x2_slide = x2[j : len(x1)]
    prod = DotProd(x1_slide, x2_slide)/i
    return prod

def MaximiseCrossCorr(x1, x2):
    stats = {}
    for i in range(1, len(x1)):
        j = len(x1) - i
        stats[i] = CorrOfHalfSlide(x1, x2, i, j)
        stats[-j] = CorrOfHalfSlide(x2, x1, i, j)
    return stats

def ElementShannonEntropy(p):
    if p != 0:
        return p * math.log2(1/p)
    else:
        return 0

def ElementMutualInformation(p, p_conditional):
    return ElementShannonEntropy(p) - ElementShannonEntropy(p_conditional)
