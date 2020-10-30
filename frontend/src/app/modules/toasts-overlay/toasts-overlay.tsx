import Toast from "app/common/components/toast/toast";
import { RootStore } from "app/common/types/store.types";
import { removeToast } from "app/modules/toasts-overlay/store/actions";
import cn from "classnames";
import React from "react";
import { connect, ConnectedProps } from "react-redux";

import "./toasts-overlay.scss";

class ToastsOverlay extends React.Component<Props> {
	toastHeight = 50;
	toastMargin = 10;
	overlayPaddingTop = 24;

	render() {
		return (
			<div className={cn("toasts-overlay")}>
				{this.props.toastList.map((toast, index) => (
					<Toast
						key={toast.id}
						id={toast.id}
						toast={toast}
						onTimeExpired={this.props.removeToast}
						style={{
							top: this.overlayPaddingTop + index * (this.toastHeight + this.toastMargin),
							height: this.toastHeight,
							maxHeight: this.toastHeight,
						}}
					/>
				))}
			</div>
		);
	}
}

const mapStateToProps = (state: RootStore) => ({
	toastList: state.toasts.toastList,
});

const mapDispatchToProps = {
	removeToast,
};

const connector = connect(mapStateToProps, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;

type Props = PropsFromRedux;

export default connector(ToastsOverlay);
