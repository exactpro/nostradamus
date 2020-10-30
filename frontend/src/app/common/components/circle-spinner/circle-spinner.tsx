import React from "react";
import cn from "classnames";

import "./circle-spinner.scss";

enum CircleSpinnerSize {
	little = 24,
	normal = 32,
	big = 62,
}

interface CircleSpinnerProps {
	size: number; // TODO: refactor to make size flexible
	alignCenter: boolean;
	className?: string;
}

class CircleSpinner extends React.Component<CircleSpinnerProps> {
	static defaultProps = {
		size: CircleSpinnerSize.big,
		alignCenter: true,
	};

	render() {
		const style = {
			width: `${this.props.size}px`,
			height: `${this.props.size}px`,
			borderWidth: `${this.props.size * 0.08}px`,
		};

		if (this.props.alignCenter) {
			return (
				<div className={cn("circle-spinner__wrapper", this.props.className)}>
					<div className="circle-spinner" style={style} />
				</div>
			);
		}
		return <div className={cn("circle-spinner", this.props.className)} style={style} />;
	}
}

export default CircleSpinner;
