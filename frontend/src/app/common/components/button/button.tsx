import React from 'react';
import cn from 'classnames';
import 'app/common/components/button/button.scss';
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";

export enum ButtonStyled {
  Primary = 'button__primary',
  Flat = 'button__flat'
}

// TODO: rewrite to props.child
type ButtonProps = {
  text: string;
  type: 'submit' | 'button' | 'reset';
  styled: ButtonStyled,
  icon?: IconType;
  className?: string;
  id?: string;
  disabled?: boolean;
  onClick?: () => void;
  iconSize?: IconSize | number;
  selected?: boolean
}

class Button extends React.Component<ButtonProps> {

  static defaultProps = {
    type: 'button',
    styled: ButtonStyled.Primary
  };

  render() {
    return (
      <button
        className={cn("button", this.props.className, this.props.styled, { 'selected': this.props.selected })}
        id={this.props.id}
        type={this.props.type}
        disabled={this.props.disabled || this.props.selected }
        onClick={this.props.onClick || undefined}
      >
        {
          this.props.icon &&
          <Icon className="button__icon" size={this.props.iconSize || IconSize.big} type={this.props.icon}/>
        }

        <span className="button__text">
          { this.props.text }
        </span>
      </button>
    );
  }
}

export default Button;
