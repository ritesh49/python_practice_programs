from tasks import add

print('Adding Integer Numbers')
a = add.delay(1, 4)
a.then(lambda res: print('Result in lambda promise ==>', res.get()))
print('Added numbers with celery ===>', a)
# print('a.ready()', a.on_ready.then(lambda res: print('Result in lambda promise ==>', res)))
print('a result =-->', a.get())
print('Backend ===>', a.backend)
