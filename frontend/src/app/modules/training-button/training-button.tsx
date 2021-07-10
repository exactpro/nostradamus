import CircleSpinner from "app/common/components/circle-spinner/circle-spinner";
import Icon, { IconSize, IconType } from "app/common/components/icon/icon";
import { isOneOf } from "app/common/functions/helper";
import { startTrainModel } from "app/common/store/traininig/thunks";
import { HttpStatus } from "app/common/types/http.types";
import { RootStore } from "app/common/types/store.types";
import cn from "classnames";
import React from "react";
import { connect, ConnectedProps } from "react-redux";

import "./training-button.scss";

interface DirectProps {
	className?: string;
}

class TrainingButton extends React.PureComponent<Props> {

	trainModel =  () => {
		this.props.startTrainModel();
	};

	render() {
		const { className, status } = this.props;

		let classStatus = "";
		let text;
		let icon;

		switch (status) {
			case HttpStatus.PREVIEW: {
				text = "Train Model";
				icon = IconType.trainModel;
				classStatus = "_preview";
				break;
			}

			case HttpStatus.LOADING: {
				text = "Searching model...";
				icon = IconType.trainModel;
				classStatus = "_loading";
				break;
			}

			case HttpStatus.RELOADING: {
				text = "Model is training...";
				icon = IconType.trainModel;
				classStatus = "_loading";
				break;
			}

			case HttpStatus.FINISHED: {
				text = "Model is trained";
				icon = IconType.check;
				classStatus = "_success";
				break;
			}

			case HttpStatus.FAILED: {
				text = "Model is not trained";
				icon = IconType.exclam;
				classStatus = "_error";
				break;
			}

			default: {
				text = "Train Model";
				icon = IconType.trainModel;
				break;
			}
		}

		const loading = isOneOf<HttpStatus>(status, [HttpStatus.LOADING, HttpStatus.RELOADING]);

		return (
			<button
				type="button"
				className={cn("training-button", `training-button${classStatus}`, className)}
				onClick={this.trainModel}
			>
				{loading && (
					<CircleSpinner size={50} alignCenter={false} className="training-button__spinner" />
				)}

				<div className="training-button__icon-container">
					<Icon
						type={icon}
						size={loading ? IconSize.normal : IconSize.big}
						className="training-button__icon"
					/>
				</div>

				{text}
			</button>
		);
	}
}

const mapStateToProps = (store: RootStore) => ({
	status: store.training.status
});

const mapDispatchToProps = {
	startTrainModel
}

const connector = connect(mapStateToProps, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;

type Props = PropsFromRedux & DirectProps;

export default connector(TrainingButton);
