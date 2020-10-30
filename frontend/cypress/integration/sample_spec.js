describe("The Home Page", () => {
	it("successfully loads", () => {
		cy.visit("http://localhost:3000"); // change URL to match your dev URL
	});

	it("registration form is opened", () => {
		cy.get("a > .button").click();
	});

	it("registration form is filled", () => {
		cy.get("#sign-up_team").select("Nostradamus");
		cy.get("#sign-up__e-mail").type("fake@email.com");
		cy.get("#sign-up__username").type("mr_geadev");
		cy.get("#sign-up__password").type("ibivul74");

		cy.get("#sign-up__submit").should("not.be.disabled");
	});
});
