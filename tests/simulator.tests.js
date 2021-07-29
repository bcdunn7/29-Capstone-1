describe("Payments test", function() {

    it('should set initial values to zero on getInitialDataset()', function () {  
        
        datasets = [
            {data: [0,1,2,3,4]},
            {data2: [0,1,2,3,4]}
        ]

        const res = getInitialDataset(datasets)

        expect(res.length()).toEqual(2);
        expect(res[0]['data']).toEqual('[0]');
    });

    afterEach(function() {
        ;
    })

  });