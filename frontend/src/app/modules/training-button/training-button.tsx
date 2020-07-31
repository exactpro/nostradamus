import { AnalysisAndTrainingApi } from 'app/common/api/analysis-and-training.api';
import CircleSpinner from 'app/common/components/circle-spinner/circle-spinner';
import Icon, { IconSize, IconType } from 'app/common/components/icon/icon';
import { isOneOf } from 'app/common/functions/helper';
import { HttpError, HttpStatus } from 'app/common/types/http.types';
import { addToast } from 'app/modules/toasts-overlay/store/actions';
import { ToastStyle } from 'app/modules/toasts-overlay/store/types';
import cn from 'classnames';
import React from 'react';
import { connect, ConnectedProps } from 'react-redux';
import { setStatusTrainModelQAMetrics } from "app/common/store/qa-metrics/actions"; 
 
import './training-button.scss';

interface InnerProps {
	className?: string,
	dashboardStatus: HttpStatus
}

interface State {
	trainingStatus: HttpStatus
}

class TrainingButton extends React.Component<Props, State> {

	state = {
		trainingStatus: HttpStatus.PREVIEW
	}

	trainModel = async () => {
		this.setState({ trainingStatus: HttpStatus.LOADING })
		this.props.addToast('Start training', ToastStyle.Info)

		try {
			let res = await AnalysisAndTrainingApi.trainModel();
			
			if(res.result === "success") this.props.setStatusTrainModelQAMetrics(true);
			this.setState({ trainingStatus: HttpStatus.FINISHED });
			
		} catch (e) {
			this.props.addToast((e as HttpError).detail || e.message, ToastStyle.Warning)
			this.setState({ trainingStatus: HttpStatus.FAILED })
		}
	}

	render() {
		let { trainingStatus } = this.state;

		let text;
		let classStatus;
		let icon;

		switch (trainingStatus) {
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

		let loading = isOneOf<HttpStatus>(trainingStatus, [HttpStatus.LOADING, HttpStatus.RELOADING]);

		return (
			<button
				type="button" className={cn('training-button', 'training-button' + classStatus, this.props.className)}
				onClick={this.trainModel}
				disabled={this.props.dashboardStatus !== HttpStatus.FINISHED}
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

const connector = connect(
	() => ({}),
	{ 
		addToast,
	  	setStatusTrainModelQAMetrics 
	},
);

type PropsFromRedux = ConnectedProps<typeof connector>

type Props = PropsFromRedux & InnerProps;

export default connector(TrainingButton);
