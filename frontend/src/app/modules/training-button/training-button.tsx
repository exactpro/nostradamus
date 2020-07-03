import CircleSpinner from 'app/common/components/circle-spinner/circle-spinner';
import Icon, { IconSize, IconType } from 'app/common/components/icon/icon';
import { isOneOf } from 'app/common/functions/helper';
import { HttpStatus } from 'app/common/types/http.types';
import { RootStore } from 'app/common/types/store.types';
import { trainModel } from 'app/modules/training-button/store/thunks';
import React from 'react';
import cn from 'classnames';
import { connect, ConnectedProps } from 'react-redux';

import './training-button.scss';

interface InnerProps {
	className?: string
}

class TrainingButton extends React.Component<Props> {

	render() {
		let { status } = this.props;

		let text;
		let classStatus;
		let icon;

		switch (status) {
			case HttpStatus.PREVIEW : {
				text = 'Train Model';
				icon = IconType.trainModel;
				classStatus = '_preview';
				break;
			}

			case HttpStatus.LOADING : {
				text = 'Model is training...';
				icon = IconType.trainModel;
				classStatus = '_loading';
				break;
			}

			case HttpStatus.FINISHED : {
				text = 'Model is trained';
				icon = IconType.check;
				classStatus = '_success';
				break;
			}

			case HttpStatus.FAILED : {
				text = 'Model is not trained';
				icon = IconType.exclam;
				classStatus = '_error';
				break;
			}

			default : {
				text = 'Train Model';
				icon = IconType.trainModel;
				break;
			}
		}

		let loading = isOneOf<HttpStatus>(status, [HttpStatus.LOADING, HttpStatus.RELOADING]);

		return (
			<button
				type="button" className={cn('training-button', 'training-button' + classStatus, this.props.className)}
				onClick={this.props.trainModel}
				disabled={this.props.btsStatus !== HttpStatus.FINISHED}
			>
				{
					loading &&
          <CircleSpinner size={50} alignCenter={false} className="training-button__spinner" />
				}

				<div className="training-button__icon-container">
					<Icon type={icon} size={loading ? IconSize.normal : IconSize.big} className="training-button__icon" />
				</div>

				{text}

			</button>
		);
	}
}

const mapStateToProps = (state: RootStore) => ({
	status: state.analysisAndTraining.trainingModel.status,
	btsStatus: state.analysisAndTraining.analysisAndTraining.status,
});

const mapDispatchToProps = {
	trainModel,
};

const connector = connect(
	mapStateToProps,
	mapDispatchToProps,
);

type PropsFromRedux = ConnectedProps<typeof connector>

type Props = PropsFromRedux & InnerProps;

export default connector(TrainingButton);
