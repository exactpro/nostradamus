import user from "../../fixtures/user.json";

describe('Collecting data', () => {

    it('Go to page with loaded data', () => {
        cy.server()
        cy.route({
            url: '/api/analysis_and_training',
            method: 'GET',
            response: {},
        })

        localStorage.setItem('user', JSON.stringify(user));
        cy.visit(Cypress.env('HOST_FOR_TEST'));
        cy.url().should('include', '/app/analysis-and-training');
    })

    it ('Show coffee machine screen', () => {
        cy.get('.at-page__collecting-data')
    })
});
