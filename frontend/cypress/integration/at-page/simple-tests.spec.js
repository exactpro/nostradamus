import user from "./../../fixtures/user.json";

describe("Simple tests", () => {
	it("redirect is correctly work", () => {
		localStorage.setItem("user", JSON.stringify(user));
		cy.visit(Cypress.env("HOST_FOR_TEST"));
		cy.url().should("include", "/app/analysis-and-training");
	});

	it("sidebar elements is rendered", () => {
		cy.get(".navigation-bar").should(($sidebar) => {
			expect($sidebar).to.contain("Analysis & Training");
			expect($sidebar).to.contain("Description Assessment");
			expect($sidebar).to.contain("QA Metrics");
			expect($sidebar).to.contain("Ask Nostradamus");
			expect($sidebar).to.contain("Settings");
		});

		cy.get(".navigation-bar__user-data").should(($userBlock) => {
			expect($userBlock, "Name is correctly").to.contain(user.name);
			expect($userBlock, "Email is correctly").to.contain(user.email);
		});
	});

	it("a&t page elements is rendered", () => {
		cy.get(".at-page .header__title").contains("Analysis & Training");
	});
});
