with open('CL_expirations_and_settlements.txt','w') as output:
    ### Table 1 output (B-records) ###

    column_width = 11
    column_label_1 = ['Futures', 'Contract', 'Contract', 'Futures', 'Options', 'Options']
    column_label_2 = ['Code', 'Month', 'Type', 'Exp Date', 'Code', 'Exp Date']
    column_label_3 = ['-------', '--------', '--------', '--------', '-------', '--------']

    # print header
    for column_label in column_label_1:
        output.write(column_label.ljust(column_width))
    output.write('\n')

    for column_label in column_label_2:
        output.write(column_label.ljust(column_width))
    output.write('\n')

    for column_label in column_label_3:
        output.write(column_label.ljust(column_width))
    output.write('\n')


    # print data
    for row in data_1:
        for value in row:
            output.write(str(value).ljust(column_width))
        output.write('\n')
        
    # Separate for good measure
    output.write('\n')
    output.write('\n')
        
    ### Table 2 output (81-records) ###
    column_width = 11
    column_label_1 = ['Futures', 'Contract', 'Contract', 'Strike', 'Settlement']
    column_label_2 = ['Code', 'Month', 'Type', 'Price', 'Price']
    column_label_3 = ['-------', '--------', '--------', '------', '----------']

    # print header
    for column_label in column_label_1:
        output.write(column_label.ljust(column_width))
    output.write('\n')

    for column_label in column_label_2:
        output.write(column_label.ljust(column_width))
    output.write('\n')

    for column_label in column_label_3:
        output.write(column_label.ljust(column_width))
    output.write('\n')


    # print data
    for row in data_2:
        for value in row:
            output.write(str(value).ljust(column_width))
        output.write('\n')