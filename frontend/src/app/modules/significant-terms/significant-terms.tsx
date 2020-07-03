import { TagCloud } from 'app/common/components/charts/tag-cloud/tag-cloud';
import CircleSpinner from 'app/common/components/circle-spinner/circle-spinner';
import Icon, { IconType } from 'app/common/components/icon/icon';
import { HttpStatus } from 'app/common/types/http.types';
import { RootStore } from 'app/common/types/store.types';
import { updateTerms } from 'app/modules/significant-terms/store/thunk';
import React from 'react';
import { connect, ConnectedProps } from 'react-redux';

import './significant-terms.scss';

class SignificantTerms extends React.PureComponent<Props> {

	changeSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
		this.props.updateTerms(String(e.target.value));
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
                  value={this.props.chosen_metric}
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

const mapStateToProps = (state: RootStore) => ({
	terms: state.analysisAndTraining.significantTerms.terms,
	chosen_metric: state.analysisAndTraining.significantTerms.chosen_metric,
	metrics: state.analysisAndTraining.significantTerms.metrics,
	status: state.analysisAndTraining.significantTerms.status,
});

const mapDispatchToProps = {
	updateTerms,
};

const connector = connect(
	mapStateToProps,
	mapDispatchToProps,
);

type PropsFromRedux = ConnectedProps<typeof connector>

type Props = PropsFromRedux & {};

export default connector(SignificantTerms);
