/* eslint-disable jsx-a11y/tabindex-no-positive */
/* eslint-disable jsx-a11y/no-noninteractive-tabindex */
// TODO: Rewrite as a functional component
import React, { Component, CSSProperties } from "react";
import "app/modules/settings/elements/input-element/input-element.scss";
import { FilterElementType } from "app/modules/settings/elements/elements-types";
import Icon, { IconSize, IconType } from "app/common/components/icon/icon";
import cn from "classnames";

interface InputElementProps {
	type: FilterElementType;
	placeholder: string;
	style: CSSProperties;
	value: string;
	onChange: (value: string) => void;
	onClear?: () => void;
	onKeyPress?: (e: React.KeyboardEvent<HTMLInputElement>) => void;
	onBlur?: (e: React.FocusEvent<HTMLInputElement>) => void;
}

// eslint-disable-next-line react/prefer-stateless-function
class InputElement extends Component<InputElementProps> {
	// eslint-disable-next-line react/static-property-placement
	static defaultProps = {
		type: FilterElementType.simple,
		placeholder: "Name",
		onChange: () => ({}),
		value: "",
		style: {},
	};

	render() {
		const { type, style, placeholder, value, onBlur, onChange, onKeyPress, onClear } = this.props;

		const allowedClearing: boolean = [FilterElementType.simple, FilterElementType.edited].includes(
			type
		);

		return (
			<div className="input-element" style={style} onBlur={onBlur} tabIndex={1}>
				<input
					className={cn("input-element__input", `input-element__input_${type}`)}
					placeholder={placeholder}
					value={value}
					disabled={![FilterElementType.simple, FilterElementType.edited].includes(type)}
					onChange={(event: React.ChangeEvent<HTMLInputElement>) => onChange(event.target.value)}
					onKeyPress={onKeyPress}
				/>
				{allowedClearing && (
					<button type="button" className="input-element__close" onClick={onClear}>
						<Icon size={IconSize.small} type={IconType.close} />
					</button>
				)}
			</div>
		);
	}
}

export default InputElement;
