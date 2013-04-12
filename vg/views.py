def get_data_from_file(id):
    """ Grab energyscan data from database """
    measurement = models.Measurement.objects.filter(Q(id__exact=id)).get()

    ES_list = energyscan.energyscan_data.split()
    k = 0
    xs = []
    ys = []
    for datapoint in ES_list:
        datapoint = datapoint.replace(',','.')
        #even -> x-value
        if k % 2 == 0:
            xs.append(float(datapoint))
        #odd -> y-value
        else:
            ys.append(float(datapoint))
        k = k + 1

    #we end at this point, because the further handling of the data depends on the function

    return energyscan, xs, ys
