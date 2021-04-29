''' this module checks for the valid input( postive numbeers > 0)
and all invalid input(other than positive integers > 0) '''
from flask import Flask ,request,jsonify


app = Flask(__name__)

@app.route('/items', methods = ["POST"] )
def items():
    ''' Takes the input from users using request.get_json()

    Parameters
    ----------
    list : list
        A list of all datatypes elements

    Returns
    -------
    dict:
        A dictionary of values  counting the frequency of valid elements and invalid elements
        along the max, min and average of valid elements also frequency of invalid elements '''
    request_data = request.get_json()
    list_items = request_data['input']
    valid_list = []
    valid_counter = 0
    invalid_counter = 0
    for i in list_items:
        if type(i) == int and i > 0:
            valid_counter += 1
            valid_list.append(i)
        if type(i) != int or i <= 0:
            invalid_counter += 1
    maximum = max(valid_list)
    minimum = min(valid_list)
    avg = sum(valid_list)/len(valid_list)
    data ={
        "valid_entries":valid_counter,
        "invalid_entries":invalid_counter,
        "min": minimum,
        "max": maximum,
        "average": avg}
    return jsonify(data)

users_slot = dict()
@app.route('/booking', methods = ["POST","GET"])
def booking():
    '''  Takes the input from users using request.get_json()

    Parameters
    ----------
    slot: int
        A slot in the form of integer in between 0 and 23
    name: str
        A name of user who will get the required allotement in available slot 
    Returns
    -------
    dict:
        if method is POST it will return with message of confirmation
        of slot OR rejection of booking 
        OR
        if method is GET it will return list of all booking at that
        particular time'''
    if request.method == "POST":
        request_data = request.get_json()
        name = request_data['name']
        slot = int( request_data['slot'])
        if slot >= 0 and slot <= 23 :
            if slot in users_slot.keys():
                if  len(users_slot[slot]) < 2:
                    users_slot[slot].append(name)
                else:
                    server_response ={ "status":"{} is full as for now".format(slot)}
                    return jsonify(server_response)  
            else:
                users_slot[slot] = [name]
            server_response = {"status":"confirmed"}
            return jsonify(server_response)
        else :
            server_response = {"status":"{} is invalid slot".format(slot)}
            return jsonify(server_response)
    else:
        return jsonify(users_slot)

@app.route('/cancel', methods = ["POST"])
def cancel():
    '''   Takes the input from users using request.get_json()

    Parameters
    ----------
    slot : int
        A slot in the form of integer in between 0 and 23
    name : str
        A name of user who want cancel the booking
    Returns
    -------
    dict:
        it will returns the message of success If the booked
        slot has been cancelled 
        OR error IF the slot or user not found in the booking list'''
    request_data = request.get_json()
    name = request_data['name']
    print(name)
    slot = int(request_data['slot'])
    if slot  in users_slot.keys():
        name_list = users_slot[slot]
        if name in name_list:
            name_list.remove(name)
            users_slot[slot] = name_list
            server_response = { "status": "canceled booking for {} in slot {}"\
                .format(name,slot)}
            return jsonify(server_response)
        else:
            server_response = {"status":"no booking for name {} found in the given slot {}"\
                .format(name,slot)}
            return jsonify(server_response)
    else: 
        server_response = {"status":"slot {} not  found".format(slot)}
        return jsonify(server_response) 
    
    
X = []     # list of x-coordinates
Y = []     # list of y-coordinates

@app.route('/plot',methods = ["POST"])
def plot():
    """Takes the input from users using request.get_json()
    Parameters
    ----------
    x : int
        get x - coordinate of point on 2D plane
    y : int
        get y-coordinate of point on 2D plane
    Returns
    -------
    str:
        a string of values  of points  that are forming  the square on 2D plane
    """
    request_data = request.get_json()
    x_coordinate = request_data['x'] 
    y_coorinate = request_data['y']   
    X.append(x_coordinate)
    Y.append(y_coorinate)
    
    if set(X) == set(Y) and len(X) >= 4 and len(Y) >= 4:
        server_response = {
        "status": "success ({},{}) ({},{}) ({},{}) ({},{}) ".\
        format(X[0], Y[0], X[1], Y[1], X[2], Y[2], X[3], Y[3])}
        return jsonify(server_response)
    else:
        if set(X) > set(Y) and len(X) >= 4 and len(Y) >= 4:      
            temp = list(set(X).difference(Y))
            for ele in range(len(temp)):
                extra = X.index(temp[ele])
                X.remove(temp[ele])
                Y.pop(extra)
            if set(X) == set(Y) and   len(X) >= 4 and len(Y) >= 4:
                server_response = {"status": "success 1 ({},{}) ({},{}) ({},{}) ({},{})"}
                return jsonify(server_response)
            

        elif set(Y) > set(X) and len(X) >= 4 and len(Y) >= 4:
            temp = list(set(Y).difference(X))
            for ele in range(len(temp)):
                extra = Y.index(temp[ele])
                Y.remove(temp[ele])
                X.pop(extra)
                if set(X) == set(Y)  and len(X) >= 4 and len(Y) >= 4:
                    server_response = {"status": "success 2 ({},{}) ({},{}) ({},{}) ({},{})"}
                    return jsonify(server_response)  
                        
    server_response = {"status":"input accepted"}
    return jsonify(server_response)
      


if __name__ == "__main__":
    app.run(debug =True)
    