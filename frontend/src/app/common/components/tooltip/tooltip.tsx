import React, { CSSProperties } from "react";
import { Timer } from "app/common/functions/timer";
import PopupComponent, {
	ChildPosition,
} from "app/common/components/popup-component/popup-component";
import cn from "classnames";

import "./tooltip.scss";

enum TooltipWrapperShowing {
	hide = "hided",
	display = "visible",
}

export enum TooltipPosition {
	top = "top",
	bottom = "bottom",
	left = "left",
	right = "right",
}

interface TooltipProps {
	duration: number;
	message: string;
	position: TooltipPosition;
	children: React.ReactNode;
	isDisplayed: boolean;
	style?: CSSProperties;
}

interface TooltipState {
	wrapperDisplayStyle: TooltipWrapperShowing;
	isReverted: boolean;
}

// Change tooltip adding approach

class Tooltip extends React.Component<TooltipProps, TooltipState> {
	static defaultProps = {
		duration: 2000,
		position: TooltipPosition.top,
		isDisplayed: true,
	};

	tooltipRef: React.RefObject<HTMLDivElement> = React.createRef<HTMLDivElement>();
	tooltipRect: DOMRect | undefined = undefined;
	timer: any = {};

	constructor(props: TooltipProps) {
		super(props);
		this.state = {
			wrapperDisplayStyle: TooltipWrapperShowing.hide,
			isReverted: false,
		};
	}

	hideTooltip = (): void => {
		this.setState({
			wrapperDisplayStyle: TooltipWrapperShowing.hide,
		});
	};

	displayTooltip = (): void => {
		if (this.timer.timerId) this.timer.close();
		const { duration } = this.props;

		this.timer = new Timer(this.hideTooltip, duration);
		this.timer.pause();

		this.setState({
			wrapperDisplayStyle: TooltipWrapperShowing.display,
		});
	};

	componentDidUpdate = () => {
		this.setTooltipRect();
		this.checkTooltipRevertStatus();
	};

	setTooltipRect = () => {
		if (!this.tooltipRef?.current) return;

		this.tooltipRect = this.tooltipRef.current.getBoundingClientRect();
	};

	checkTooltipRevertStatus = () => {
		if (!this.tooltipRect) return;

		if (
			!this.state.isReverted &&
			this.tooltipRect.left + this.tooltipRect.width > window.innerWidth
		) {
			this.setState({ isReverted: true });
		} else if (
			this.state.isReverted &&
			this.tooltipRect.right + this.tooltipRect.width <= window.innerWidth
		) {
			this.setState({ isReverted: false });
		}
	};

	render() {
		const { wrapperDisplayStyle, isReverted } = this.state;
		const { isDisplayed, children, position, style, message } = this.props;

		return (
			<div className="tooltip">
				<PopupComponent
					isChildDisplayed={wrapperDisplayStyle === TooltipWrapperShowing.display}
					childPosition={(position as unknown) as ChildPosition}
					parent={
						<div
							className={cn({ "tooltip__wrapped-object": isDisplayed })}
							onMouseEnter={this.displayTooltip}
							onMouseLeave={this.timer.resume}
						>
							{children}
						</div>
					}
					child={
						<div
							className={cn(
								"tooltip-wrapper",
								{ "tooltip-wrapper_displayed": isDisplayed },
								`tooltip-wrapper_${position}`,
								`tooltip-wrapper_${position}${isReverted ? "-reverted" : ""}`,
								`tooltip-wrapper_${wrapperDisplayStyle}`
							)}
							style={style}
							onMouseEnter={this.timer.pause}
							onMouseLeave={this.timer.resume}
							ref={this.tooltipRef}
						>
							<p className="tooltip-wrapper__content">{message}</p>
							<div
								className={cn("tooltip-wrapper__triangle", `tooltip-wrapper__triangle_${position}`)}
							/>
						</div>
					}
				/>
			</div>
		);
	}
}

export default Tooltip;
