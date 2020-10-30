/* eslint-disable jsx-a11y/tabindex-no-positive */
/* eslint-disable jsx-a11y/no-noninteractive-tabindex */
import React, { Component } from "react";
import { FilterElementType } from "app/modules/settings/elements/elements-types";
import Icon, { IconSize, IconType } from "app/common/components/icon/icon";
import cn from "classnames";
import "app/common/components/native-components/dropdown-element/dropdown-element.scss";
import { caseInsensitiveStringCompare } from "app/common/functions/helper";

interface DropdownProps {
	type: FilterElementType;
	value: string;
	dropDownValues: string[];
	writable: boolean;
	excludeValues: string[];
	onChange: (s: string) => void;
	onClear?: () => void;
	style?: React.CSSProperties;
	placeholder?: string;
}

interface DropdownState {
	inputValue: string;
	isDropDownWrapperOpened: boolean;
}

class DropdownElement extends Component<DropdownProps, DropdownState> {
	// eslint-disable-next-line react/static-property-placement
	static defaultProps = {
		type: FilterElementType.simple,
		value: "",
		writable: true,
		excludeValues: [],
		placeholder: "Type",
	};

	dropdownElementRef: React.RefObject<HTMLDivElement> = React.createRef();

	constructor(props: DropdownProps) {
		super(props);
		this.state = {
			inputValue: props.value,
			isDropDownWrapperOpened: false,
		};
	}

	focusDropDownElement = (): void => {
		this.setState({ isDropDownWrapperOpened: true });
	};

	blurDropDownElement = (): void => {
		this.setState({ isDropDownWrapperOpened: false });
	};

	selectDropdownOption = (inputValue: string) => (): void => {
		const { onChange, writable } = this.props;

		this.setState({ inputValue }, this.blurDropDownElement);
		onChange(inputValue);

		if (!writable && this.dropdownElementRef.current) this.dropdownElementRef.current.blur();
	};

	changeInputValue = (e: React.ChangeEvent<HTMLInputElement>): void => {
		this.setState({ inputValue: e.target.value });
	};

	clearInputValue = (): void => {
		const { onClear } = this.props;
		this.setState({ inputValue: "" }, onClear);
	};

	shouldComponentUpdate = (nextProps: DropdownProps): boolean => {
		const { value } = this.props;
		if (!nextProps.value.length && value) this.setState({ inputValue: "" });
		if (nextProps.value !== value) this.setState({ inputValue: nextProps.value });
		return true;
	};

	isStrIncludesSubstr = (str: string, substr: string): boolean =>
		str.toLowerCase().includes(substr.toLowerCase());

	render() {
		const {
			type,
			writable,
			dropDownValues,
			excludeValues,
			style,
			placeholder,
			value,
			onClear,
		} = this.props;
		const { inputValue, isDropDownWrapperOpened } = this.state;

		const allowedOpening: boolean = [FilterElementType.simple, FilterElementType.edited].includes(
			type
		);

		const hasIcon = [
			FilterElementType.simple,
			FilterElementType.edited,
			FilterElementType.disabled,
		].includes(type);

		const isInputEditable: boolean = allowedOpening && writable;

		let dropDownOptions: string[] = [...dropDownValues];

		if (isInputEditable) {
			dropDownOptions = dropDownOptions.filter((str: string) => {
				if (inputValue.length)
					return this.isStrIncludesSubstr(str, inputValue) && !excludeValues?.includes(str);
				return true;
			});
		}

		dropDownOptions.sort((a, b) => caseInsensitiveStringCompare(a, b));

		return (
			<div
				className="dropdown-element"
				tabIndex={1}
				ref={this.dropdownElementRef}
				onFocus={this.focusDropDownElement}
				onBlur={this.blurDropDownElement}
				style={style}
			>
				<input
					value={inputValue}
					onChange={this.changeInputValue}
					placeholder={placeholder}
					disabled={!isInputEditable}
					className={cn("dropdown-element__select", `dropdown-element__select_${type}`, {
						"dropdown-element__select_disabled": !value,
					})}
				/>

				{allowedOpening && (
					<>
						{!!dropDownOptions.length && (
							<div
								className={cn("dropdown-element-wrapper", {
									"dropdown-element-wrapper_hidden": !isDropDownWrapperOpened,
								})}
							>
								{dropDownOptions.map((item) => (
									// eslint-disable-next-line jsx-a11y/no-static-element-interactions
									<div
										className={cn("dropdown-element-wrapper__option", {
											"dropdown-element-wrapper__option_disabled":
												!inputValue.length && excludeValues?.includes(item),
										})}
										onKeyDown={() => ({})}
										onClick={this.selectDropdownOption(item)}
										key={item}
									>
										{item}
									</div>
								))}
							</div>
						)}
					</>
				)}

				{hasIcon && (
					<Icon
						className={cn("dropdown-element__open", {
							"dropdown-element__open_rotated": allowedOpening && isDropDownWrapperOpened,
						})}
						size={IconSize.small}
						type={IconType.down}
					/>
				)}

				{hasIcon && onClear && (
					<button
						type="button"
						className="dropdown-element__clear-value"
						onClick={this.clearInputValue}
					>
						<Icon size={IconSize.small} type={IconType.close} />
					</button>
				)}
			</div>
		);
	}
}

export default DropdownElement;
