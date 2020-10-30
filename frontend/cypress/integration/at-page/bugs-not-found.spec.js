import emptyFilter from "../../fixtures/at-page/empty-filters.json";
import user from "../../fixtures/user.json";

describe("Filtered bugs is 0", () => {
	it("Go to page with loaded data", () => {
		localStorage.setItem("user", JSON.stringify(user));

		cy.server();
		cy.route({
			url: "/api/analysis_and_training",
			method: "GET",
			response: { records_count: { total: 55173, filtered: 0 } },
		});

		cy.route({
			url: "/api/analysis_and_training/filter/",
			method: "GET",
			response: emptyFilter,
		});

		cy.visit(Cypress.env("HOST_FOR_TEST"));
		cy.url().should("include", "/app/analysis-and-training");
	});

	it("Notification is showed", () => {
		cy.get(".toast")
			.should("have.class", "toast toast_styled_warn")
			.contains("With cached filters we didn't find data. Try to change filter.");
	});

	it("Statistic is correctly", () => {
		cy.get(".at-page__main-statistic").should(($mainStatistic) => {
			expect(
				$mainStatistic.find(".main-statistic__number_type_total"),
				"Total count is correctly"
			).to.contain("55173");
			expect(
				$mainStatistic.find(".main-statistic__number_type_filtered"),
				"Total count is correctly"
			).to.contain("0");
		});
	});

	it("Cards on preview", () => {
		cy.get(".card.configuration-tab  .card__content").should("not.be.empty");

		cy.get(".card.statistics  .card__content").should("be.empty");

		cy.get(".card.defect-submission-card  .card__content").should("be.empty");

		cy.get(".card.frequently-used-terms  .card__content").should("be.empty");

		cy.get(".card.at-page__significant-terms  .card__content").should("be.empty");
	});
});
