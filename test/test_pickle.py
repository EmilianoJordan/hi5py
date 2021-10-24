# def test_numpy_object():
#     a = np.random.rand(3, 3, 3).astype("O")
#
#     a[0, :, :] = [["string"] * 3] * 3
#
#     buffer = BytesIO()
#     to_file(a, buffer)
#     result = from_file(buffer)
#
#     print(result)
