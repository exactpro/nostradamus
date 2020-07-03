import React from 'react';

import Card from 'app/common/components/card/card';
import { HttpStatus } from 'app/common/types/http.types';

import Header from 'app/modules/header/header';

import bugResolutionPreview from 'assets/images/dAssessment__bug-resolution__preview.png';
import priorityPreview from 'assets/images/dAssessment__priority__preview.png';
import testingProbabilityPreview from 'assets/images/dAssessment__testing-probability__preview.png';
import textFieldPreview from 'assets/images/dAssessment__text-field__preview.png';
import ttrPreview from 'assets/images/dAssessment__ttr__preview.png';

import './description-assessment.page.scss';

class DescriptionAssessmentPage extends React.Component {

	render() {
		return (
			<div className="dAssessment-page">
				<Header pageTitle="Description Assessment" />

				<div className="dAssessment-page__content">
					<div className="dAssessment-page__column dAssessment-page__column_position_left">
						<Card
							previewImage={textFieldPreview}
							status={HttpStatus.PREVIEW}
							className="text-field dAssessment-page__card"
						>
							{/*text field with backlight*/}
						</Card>

						<Card
							previewImage={testingProbabilityPreview} title="Area Of Testing Probability"
							status={HttpStatus.PREVIEW}
							className="probability dAssessment-page__card"
						>
						</Card>

					</div>

					<div className="dAssessment-page__column dAssessment-page__column_position_right">
						<Card
							previewImage={bugResolutionPreview} title="Bug Resolution"
							status={HttpStatus.PREVIEW}
							className="bug-resolution dAssessment-page__card"
						>
						</Card>

						<Card
							previewImage={priorityPreview} title="Priority"
							status={HttpStatus.PREVIEW}
							className="priority dAssessment-page__card"
						>
						</Card>

						<Card
							previewImage={ttrPreview} title="Time to Resolve (TTR)"
							status={HttpStatus.PREVIEW}
							className="ttr dAssessment-page__card"
						>
						</Card>
					</div>
				</div>
			</div>
		);
	}
}

export default DescriptionAssessmentPage;
