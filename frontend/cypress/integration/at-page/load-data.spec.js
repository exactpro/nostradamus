import user from "../../fixtures/user.json";

import emptyFilter from "../../fixtures/at-page/empty-filters.json";
import defectSubmission from "../../fixtures/at-page/defect-submission.json";
import frequentlyTerms from "../../fixtures/at-page/frequently-terms.json";
import statistic from "../../fixtures/at-page/statistic.json";
import significantTerms from "../../fixtures/at-page/significant-terms.json";


describe('Load Not Filtered Data', () => {

    it('Go to page with loaded data', () => {
        localStorage.setItem('user', JSON.stringify(user));

        cy.server()
        cy.route({
            url: '/api/analysis_and_training',
            method: 'GET',
            response: {"records_count":{"total":55173,"filtered": 55173}},
        })

        cy.route({
            url: '/api/analysis_and_training/filter/',
            method: 'GET',
            response: emptyFilter,
        })

        cy.route({
            url: '/api/analysis_and_training/frequently_terms/',
            method: 'GET',
            response: frequentlyTerms,
        })

        cy.route({
            url: '/api/analysis_and_training/statistics/',
            method: 'GET',
            response: statistic,
        })

        cy.route({
            url: '/api/analysis_and_training/defect_submission/',
            method: 'GET',
            response: defectSubmission,
        })

        cy.route({
            url: '/api/analysis_and_training/significant_terms/',
            method: 'GET',
            response: significantTerms,
        })

        cy.visit(Cypress.env('HOST_FOR_TEST'));
        cy.url().should('include', '/app/analysis-and-training');
    })

    it('Statistic is correctly', () => {
        cy.get('.at-page__main-statistic').should(($mainStatistic) => {
            expect($mainStatistic.find('.main-statistic__number_type_total'), 'Total count is correctly').to.contain('55173');
            expect($mainStatistic.find('.main-statistic__number_type_filtered'), 'Total count is correctly').to.contain('55173');
        });
    })

    it('Cards isn\'t on preview', () => {
        cy.get('.card.configuration-tab  .card__content')
            .should('not.be.empty')

        cy.get('.card.statistics  .card__content')
            .should('not.be.empty')

        cy.get('.card.defect-submission-card  .card__content')
            .should('not.be.empty')

        cy.get('.card.frequently-used-terms  .card__content')
            .should('not.be.empty')

        cy.get('.card.at-page__significant-terms  .card__content')
            .should('not.be.empty')
    })

    it('Statistic is work', () => {

        cy.get('.card.statistics  .card__content')
            .should(($statistic) => {
                expect($statistic, 'Comments is showed').to.contain('Comments');
                expect($statistic, 'Attachments is showed').to.contain('Attachments');
                expect($statistic, 'Time to Resolve is showed').to.contain('Time to Resolve');
            })
    })
});
