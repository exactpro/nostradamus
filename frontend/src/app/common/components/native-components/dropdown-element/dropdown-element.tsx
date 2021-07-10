/* eslint-disable jsx-a11y/tabindex-no-positive */
/* eslint-disable jsx-a11y/no-noninteractive-tabindex */
import React, { Component } from "react";
import { FilterElementType } from "app/modules/settings/elements/elements-types";
import Icon, { IconSize, IconType } from "app/common/components/icon/icon";
import cn from "classnames";
import "app/common/components/native-components/dropdown-element/dropdown-element.scss";
import { caseInsensitiveStringCompare } from "app/common/functions/helper";

interface DropdownVariant {
	value: string;
	label: string;
}

type DropdownVariantsType = Array<string | DropdownVariant>;

interface DropdownProps {
	type: FilterElementType;
	value: string | DropdownVariant;
	dropDownValues: DropdownVariantsType;
	writable: boolean;
	excludeValues: string[];
	onChange: (s: string) => void;
	onClear?: () => void;
	style?: React.CSSProperties;
	placeholder?: string;
	className?: string;
}

interface DropdownState {
	inputValue: string | DropdownVariant;
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

	selectDropdownOption = (newValue: string | DropdownVariant) => (): void => {
		const { onChange, writable } = this.props;

		this.setState({ inputValue: newValue }, this.blurDropDownElement);
		onChange(typeof newValue === 'string' ? newValue : newValue.value);

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
		let value  = typeof this.props.value === "string" ? this.props.value : this.props.value.value;
		let newValue  = typeof nextProps.value === "string" ? nextProps.value : nextProps.value.value;

		if (!newValue.length && value) this.setState({ inputValue: "" });
		if (newValue !== value) this.setState({ inputValue: nextProps.value });
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

		let dropDownOptions: DropdownVariantsType = [...dropDownValues];

		if (isInputEditable) {
			dropDownOptions = dropDownOptions.filter((variant: string | DropdownVariant) => {
				let inputValueTemp = typeof inputValue === "string" ? inputValue : inputValue.value;
				if (inputValueTemp.length) {
					if (typeof variant === "string") {
						return (
							this.isStrIncludesSubstr(variant, inputValueTemp) && !excludeValues?.includes(variant)
						);
					} else {
						return (
							this.isStrIncludesSubstr(variant.value, inputValueTemp) &&
							!excludeValues?.includes(variant.value)
						);
					}
				}
				return true;
			});
		}

		dropDownOptions.sort((a, b) => {
			return caseInsensitiveStringCompare(
				typeof a === "string" ? a : a.value,
				typeof b === "string" ? b : b.value
			);
		});

		return (
			<div
				className={cn('dropdown-element', this.props.className)}
				tabIndex={1}
				ref={this.dropdownElementRef}
				onFocus={this.focusDropDownElement}
				onBlur={this.blurDropDownElement}
				style={style}
			>
				<input
					value={typeof inputValue === "string" ? inputValue : inputValue.label}
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
								{dropDownOptions.map((item) => {
									// eslint-disable-next-line jsx-a11y/no-static-element-interactions

									let label = typeof item === 'string' ? item : item.label;
									let value = typeof item === 'string' ? item : item.value;
									let inputValueTemp = typeof inputValue === "string" ? inputValue : inputValue.value;

									return (
										<div
											className={cn("dropdown-element-wrapper__option", {
												"dropdown-element-wrapper__option_disabled":
													!inputValueTemp.length && excludeValues?.includes(value),
											})}
											onKeyDown={() => ({})}
											onClick={this.selectDropdownOption(item)}
											key={value}
										>
											{label}
										</div>
									);
								})}
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
