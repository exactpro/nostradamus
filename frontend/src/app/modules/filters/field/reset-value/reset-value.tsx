import Icon, { IconSize, IconType } from "app/common/components/icon/icon";
import "app/modules/filters/field/reset-value/reset-value.scss";
import cn from "classnames";
import React from "react";

interface Props {
	className?: string;
	onClick?: () => void;
}

class ResetValue extends React.PureComponent<Props> {
	render() {
		return (
			<button className={cn("reset-value", this.props.className)} onClick={this.props.onClick}>
				<Icon type={IconType.close} size={IconSize.small} />
			</button>
		);
	}
}

export default ResetValue;
