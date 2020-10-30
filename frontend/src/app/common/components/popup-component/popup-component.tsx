/* eslint-disable @typescript-eslint/no-unsafe-assignment */
/* eslint-disable consistent-return */
/* eslint-disable react/static-property-placement */
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
import React, { ReactNode } from "react";
import "./popup-component.scss";

export enum ChildPosition {
	top = "top",
	bottom_right = "bottom_right",
}

interface PopupComponentProps {
	isChildDisplayed: boolean;
	childPosition: ChildPosition;
	parent: ReactNode;
	child: ReactNode;
}

export default class PopupComponent extends React.Component<PopupComponentProps> {
	static defaultProps = {
		inScrollContainer: true,
		childPosition: ChildPosition.top,
	};

	parentRef: React.RefObject<HTMLDivElement> = React.createRef();
	childRef: React.RefObject<HTMLDivElement> = React.createRef();
	childCoords: any = {};
	timerID: number | undefined = undefined;

	componentDidMount = (): void => {
		this.childCoords = this.childRef.current!.getBoundingClientRect();
		this.calculateChildPosition();
	};

	clearTimeout = (): void => {
		if (this.timerID) {
			clearInterval(this.timerID);
			this.timerID = undefined;
		}
	};

	componentDidUpdate = (): void => {
		clearTimeout();
		const { isChildDisplayed } = this.props;
		if (isChildDisplayed) this.timerID = setInterval(this.calculateChildPosition, 100);
		else clearTimeout();
	};

	calculateChildPosition = (isReturned = false): any => {
		const parentCoords: DOMRect | undefined = this.parentRef.current?.getBoundingClientRect();
		const childCoeffs = this.getChildPositionCoeffs(parentCoords);

		if (!parentCoords) return {};

		if (isReturned)
			return {
				top: parentCoords.top + childCoeffs.top,
				left: parentCoords.left + childCoeffs.left,
			};
		this.childRef.current!.style.top = `${parentCoords.top + childCoeffs.top}px`;
		this.childRef.current!.style.left = `${parentCoords.left + childCoeffs.left}px`;
	};

	getChildPositionCoeffs = (parentCoords: DOMRect | undefined) => {
		const childCoeffs = { top: 0, left: 0 };
		const { childPosition } = this.props;
		if (parentCoords) {
			switch (childPosition) {
				case ChildPosition.top:
					return childCoeffs;
				case ChildPosition.bottom_right:
					return {
						top: parentCoords.height,
						left: parentCoords.width - this.childCoords.width,
					};
				default:
					return childCoeffs;
			}
		} else return childCoeffs;
	};

	render() {
		this.clearTimeout();
		const { parent, child } = this.props;
		return (
			<div className="pop-up-component">
				<div className="pop-up-component__parent" ref={this.parentRef}>
					{parent}
				</div>

				<div
					className="pop-up-component__child"
					ref={this.childRef}
					style={this.calculateChildPosition(true)}
				>
					{child}
				</div>
			</div>
		);
	}
}
