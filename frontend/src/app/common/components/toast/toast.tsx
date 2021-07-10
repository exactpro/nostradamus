import Icon, { IconType } from "app/common/components/icon/icon";
import { Timer } from "app/common/functions/timer";
import { Toast as ToastParams } from "app/modules/toasts-overlay/store/types";
import React, { CSSProperties, ReactElement, RefObject } from "react";
import cn from "classnames";
import "./toast.scss";

export type ToastProps = {
	id: number;
	onTimeExpired: (id: number) => void;
	style: CSSProperties;
	toast: ToastParams;
	className?: string;
};

interface IState {
	expandable: boolean;
	expanded: boolean;
}

class Toast extends React.Component<ToastProps, IState> {
	timer: Timer;
	messageRef: RefObject<HTMLDivElement>;
	style: CSSProperties;

	constructor(props: ToastProps) {
		super(props);

		this.state = {
			expandable: false,
			expanded: false,
		};

		this.style = props.style;

		const { toast } = this.props;
		this.timer = new Timer(this.deleteToast, toast.config.time);
		this.messageRef = React.createRef();
	}

	componentWillUnmount(): void {
		this.timer.close();
	}

	deleteToast = (): void => {
		const { props } = this;
		props.onTimeExpired(props.id);
	};

	toggleExpand = (val: boolean) => (): void => {
		this.setState((state) => ({
			expanded: state.expandable ? val : false,
		}));
	};

	// stop timer of removing, when cursor is hovered
	mouseEnterHandler = (): void => {
		this.timer.pause();
		const { style } = this.props;
		this.style = style;

		this.setState((state, props) => ({
			expandable:
				props.toast.actionToast ||
				(this.messageRef.current
					? this.messageRef.current.scrollWidth > this.messageRef.current.clientWidth
					: false),
		}));
	};

	// resume timer of removing, when the cursor is removed
	mouseLeaveHandler = (): void => {
		const { props, state } = this;
		this.timer.resume();

		this.style = props.style;
		if (state.expanded) {
			this.toggleExpand(false)();
		} else {
			this.forceUpdate();
		}
	};

	render(): ReactElement {
		const { props, state } = this;
		const { toast } = props;

		const style = this.timer.paused ? this.style : props.style;

		return (
			// eslint-disable-next-line jsx-a11y/click-events-have-key-events,jsx-a11y/no-static-element-interactions
			<div
				className={cn("toast", props.className, `toast_styled${toast.style}`, {
					toast_expandable: state.expandable,
					toast_expanded: state.expanded,
					toast_withActions: props.toast.actionToast,
				})}
				style={style}
				onMouseEnter={this.mouseEnterHandler}
				onMouseLeave={this.mouseLeaveHandler}
				onClick={this.toggleExpand(true)}
			>
				<div className="toast__message" ref={this.messageRef}>
					{toast.message}
				</div>

				{toast.actionToast && (
					<div className="toast__buttons">
						{toast.buttons.map(({ buttonName, callBack }) => (
							<button
								key={buttonName}
								type="button"
								className="toast__button"
								onClick={() => {
									callBack();
									this.deleteToast();
								}}
							>
								{buttonName}
							</button>
						))}
						<button className="toast__button" type="button" onClick={this.deleteToast}>
							Close
						</button>
					</div>
				)}

				{toast.config.hideable && !toast.actionToast && (
					// eslint-disable-next-line jsx-a11y/no-static-element-interactions,jsx-a11y/click-events-have-key-events
					<div className="toast__close" onClick={this.deleteToast}>
						<Icon type={IconType.close} size={15} />
					</div>
				)}
			</div>
		);
	}
}

export default Toast;
