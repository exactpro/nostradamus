/* eslint-disable @typescript-eslint/no-unsafe-assignment */
/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable react/static-property-placement */
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
	tooltipOuterRef?: React.RefObject<HTMLDivElement>;
}

interface TooltipState {
	wrapperDisplayStyle: TooltipWrapperShowing;
}

// Change tooltip adding approach

class Tooltip extends React.Component<TooltipProps, TooltipState> {
	static defaultProps = {
		duration: 2000,
		position: TooltipPosition.top,
		isDisplayed: true,
	};

	timer: any = {};

	constructor(props: TooltipProps) {
		super(props);
		this.state = {
			wrapperDisplayStyle: TooltipWrapperShowing.hide,
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

	render() {
		const { wrapperDisplayStyle } = this.state;
		const { isDisplayed, children, position, style, tooltipOuterRef, message } = this.props;

		return (
			<div className="tooltip">
				<PopupComponent
					isChildDisplayed={wrapperDisplayStyle === TooltipWrapperShowing.display}
					childPosition={ChildPosition.top}
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
								`tooltip-wrapper_${wrapperDisplayStyle}`
							)}
							style={style}
							onMouseEnter={this.timer.pause}
							onMouseLeave={this.timer.resume}
							ref={tooltipOuterRef}
						>
							<div className="tooltip-wrapper__content">{message}</div>
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
