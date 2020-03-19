import timeit
#cy=timeit.timeit('for i in xrange(10): oct(i)', 'gc.enable()')
cy = timeit.timeit('print("fdsafdsa")', setup='import ant', number=1)
py = timeit.timeit('for i in range(10): oct(i)', setup='import ant', number=1)

print(cy/py)
#print('Cython is {}x faster'.format(py/cy))