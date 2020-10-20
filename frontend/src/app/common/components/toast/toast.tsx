import Icon, { IconType } from 'app/common/components/icon/icon';
import { Timer } from 'app/common/functions/timer';
import { Toast as ToastParams } from 'app/modules/toasts-overlay/store/types';
import React, { CSSProperties, RefObject } from 'react';
import cn from 'classnames';
import './toast.scss';

export type ToastProps = {
	id: number
	onTimeExpired: (id: number) => void
	style: CSSProperties
	toast: ToastParams,
	className?: string;
};

interface IState {
	expandable: boolean;
	expanded: boolean
}

class Toast extends React.Component<ToastProps, IState> {

	state: Readonly<IState>;

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

		this.timer = new Timer(this.deleteToast, this.props.toast.config.time);
		this.messageRef = React.createRef();
	}

	componentWillUnmount(): void {
		this.timer.close();
	}

	deleteToast = () => {
		this.props.onTimeExpired(this.props.id);
	};

	toggleExpand = (val: boolean) => () => {
		this.setState((state)=>({
			expanded: state.expandable ? val : false,
		}));
	};

	// stop timer of removing, when cursor is hovered
	mouseEnterHandler = () => {
		this.timer.pause();
		this.style = this.props.style;

		this.setState((state, props)=>({
			expandable: props.toast.actionToast || (this.messageRef.current ? this.messageRef.current.scrollWidth > 350 : false),
		}));
	};

	// resume timer of removing, when the cursor is removed
	mouseLeaveHandler = () => {
		this.timer.resume();
		this.style = this.props.style;
		if (this.state.expanded) {
			this.toggleExpand(false)();
		} else {
			this.forceUpdate();
		}
	};

	render() {
		let { toast } = this.props;

		let style = this.timer.paused ? this.style : this.props.style;

		return (
			<div
				className={cn('toast', this.props.className, 'toast_styled' + toast.style,
					{ 'toast_expandable': this.state.expandable, 'toast_expanded': this.state.expanded,'toast_withActions' : this.props.toast.actionToast })}
				style={style}
				onMouseEnter={this.mouseEnterHandler}
				onMouseLeave={this.mouseLeaveHandler}
				onClick={this.toggleExpand(true)}
			>
				<div className="toast__message" ref={this.messageRef}>
					{toast.message}
				</div>

				{
					toast.actionToast &&
					<div className="toast__buttons">
						{
							toast.buttons.map(({ buttonName, callBack }) =>
								<button key={buttonName} className="toast__button" onClick={() => {callBack(); this.deleteToast()}}>
									{buttonName}
								</button>
							)
						}
						<button className="toast__button" onClick={this.deleteToast}>
							Close
						</button>
					</div>
				}


				{
					toast.config.hideable && !toast.actionToast &&
          <div className="toast__close" onClick={this.deleteToast}>
              <Icon type={IconType.close} size={15} />
          </div>
				}
			</div>
		);
	}
}

export default Toast;
