describe("The Auth Page", () => {
	it("successfully loads", () => {
		cy.server();
		cy.route({
			url: "/api/auth/register/",
			method: "GET",
			response: [{ id: 1, name: "Nostradamus" }],
		});

		cy.visit(Cypress.env("HOST_FOR_TEST"));
		cy.url().should("include", "/auth/sign-in");
	});

	it("registration form is opened", () => {
		cy.get("a > .button").click();
		cy.url().should("include", "/auth/sign-up");
	});

	it("registration form is filled and valid", () => {
		cy.get("#sign-up_team").select("Nostradamus");
		cy.get("#sign-up__e-mail").type("fake@email.com");
		cy.get("#sign-up__username").type("mr_geadev");
		cy.get("#sign-up__password").type("ibivul74");

		cy.get("[type=submit]").should("be.enabled");
	});

	it("registration is success", () => {
		cy.server();
		cy.route({
			url: "/api/auth/register/**",
			method: "POST",
			response: { result: "success" },
		});

		cy.get("[type=submit]").click();

		cy.url().should("include", "/auth/sign-in");
	});

	it("auth is success", () => {
		cy.server();
		cy.route({
			url: "/api/auth/signin/**",
			method: "POST",
			response: {
				id: 2,
				name: "mr_geadev",
				email: "kgk2409@gmail.com",
				team: "Nostradamus",
				role: "QA",
				token:
					"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA3NjQ0NTg2LCJqdGkiOiJmNzVjNmUxNWVlMGY0NWUzODQwZTA0NDYzZmNiZjNhMSIsImlkIjoyfQ.fQCksIklN8rRDGwYU2M3u5mSgT8Er2E2tFOSNbWUqq0",
			},
		});

		cy.get("#sign-in__credentials").type("mr_geadev");
		cy.get("#sign-in__password").type("ibivul74");
		cy.get("[type=submit]").click();

		cy.url().should("include", "/app/analysis-and-training");
	});
});
