import { AnalysisAndTrainingApi } from 'app/common/api/analysis-and-training.api';
import { TagCloud } from 'app/common/components/charts/tag-cloud/tag-cloud';
import CircleSpinner from 'app/common/components/circle-spinner/circle-spinner';
import Icon, { IconType } from 'app/common/components/icon/icon';
import { HttpStatus } from 'app/common/types/http.types';
import { Terms } from 'app/modules/significant-terms/store/types';
import React from 'react';

import './significant-terms.scss';

interface Props {
	status: HttpStatus,
	onChangeMetric: (period: string) => void,
	metrics: string[],
	chosen_metric: string | null,
	terms: Terms
}

class SignificantTerms extends React.PureComponent<Props> {

	changeSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
		this.props.onChangeMetric(String(e.target.value));
	};

	render() {
		return (
			<div className="significant-terms">
				{
					this.props.chosen_metric &&
          <label className="significant-terms__select-wrapper">
              <select
                  className="significant-terms__select"
                  id="significant-terms__select"
                  placeholder="Metric"
                  value={this.props.chosen_metric!}
                  onChange={this.changeSelect}
                  name="Metric"
              >
								{
									this.props.metrics.map((metric: string) => (
										<option className="significant-terms__option" key={metric} value={metric}>{metric}</option>
									))
								}
              </select>

              <Icon type={IconType.down} className="significant-terms__select-icon" />
          </label>
				}

				{
					this.props.status === HttpStatus.FINISHED &&
          <TagCloud tags={this.props.terms} />
				}

				{
					this.props.status === HttpStatus.RELOADING &&
          <CircleSpinner alignCenter />
				}
			</div>
		);
	}
}

export default SignificantTerms;
