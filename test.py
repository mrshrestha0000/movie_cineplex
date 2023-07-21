def seat_detail(detail):

    # seat_detail_model = models.seat_detail_model()
    # data construction 

    theatre_id = detail['theatre_id']
    audi_id = detail['audi_id']
    audi_name = detail['audi_name']
    audi_total_seat = detail['audi_total_seat']
    row = detail['row']
    column = detail['column']


    total_seat = row * column

    for i in range(row):
        row_character = chr(ord('A')+i)
        for j in range(column):
            column_number = j + 1
            seat_id = f"{row_character}{column_number}"
            seat_name = f"{theatre_id}-{audi_id}-{audi_name}-{seat_id}"
            a = seat_name.replace(" ","")
            print (a)



detail = {
        "theatre_id": 1,
        "audi_id": 1,
        "audi_name": "audi 1",
        "audi_total_seat": 100,
        "row": 5,
        "column": 5
    }
seat_detail(detail)