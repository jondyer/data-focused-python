"""
@author: Jonathan Dyer & Brian Rhindress
"""
data_1 = []
data_2 = []

# read in and write out data 
with open('cme.20190118.c.pa2', 'r') as read_file:
    # with open('CL_expirations_and_settlements.txt','w') as write_file:
    for line in read_file: 
        # B-type futures 
        if (line[0]=='B' and (line[5:15]=='CL        ' or line[5:15]=='LO        ')):
            commodity_code = line[5:7]
            contract_type = line[15:18]
            
            # check to make sure we're in the right time frame
            year = line[18:22]; month = line[22:24]
            if not (201903 <= int(line[18:24]) <= 202112):
                continue
            contract_month = year + '-' + month 
            
            
            # top half of table
            if (commodity_code=='CL'):
                options_code = ''
                futures_code = 'CL'
                
                # should be just 'FUT'
                if (contract_type != 'FUT'):
                    continue
                contract_type = contract_type[0] + contract_type[1:].lower()
                
                # get exp date
                futures_expiration_date = line[91:95] + '-' + line[95:97] + '-' + line[97:99]
                options_exp_date = ''
                
            # bottom half of table
            elif(commodity_code=='LO'):
                options_code = 'LO'
                futures_code = 'CL'
                
                # should be 'OOF'
                contract_type = 'Opt'
                
                futures_expiration_date = ''
                options_exp_date = line[91:95] + '-' + line[95:97] + '-' + line[97:99]
                
                
                
                
            data_1 += [[futures_code,contract_month,contract_type,futures_expiration_date,
                      options_code,options_exp_date]]
            
                
                
        #81-type futures
        elif(line[0:2]=='81'):
            if(line[15:25]=='CL        '):
                futures_code = line[15:17]
                
                # check to make sure we're in the right time frame
                year = line[29:33]; month = line[33:35]
                if not (201903 <= int(line[29:35]) <= 202112):
                    continue
                contract_month = year + '-' + month
                settlement_price = "0.00" if line[108:122] == "00000000000000" else (line[108:120].lstrip('0') or "0") + '.' + line[120:122]
                
                
                if (line[25:28]=='FUT'):
                    contract_type = line[25] + line[26:28].lower()
                    strike_price = ''
                    
                elif (line[25:28]=='OOF'):
                    type_of_option = line[28]
                    contract_type = 'Put' if type_of_option=='P' else 'Call'
                    
                    strike_price = (line[47:52].lstrip('0') or "0") + '.' + line[52:54]
                    
            
                data_2 += [[futures_code, contract_month, contract_type, strike_price, settlement_price]]
                


##### Now output #####
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

