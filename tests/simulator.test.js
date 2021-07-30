describe("File Testing", function() {

    it('should add a and b together on fakefunction()', function() {
        expect(fakefunction(5,6)).toEqual(11);
        expect(fakefunction(7,6)).toEqual(13);
    })
})