/* eslint-disable jsx-a11y/click-events-have-key-events */
/* eslint-disable jsx-a11y/no-static-element-interactions */
/* eslint-disable react/require-default-props */
import React, { ReactElement } from "react";
import cn from "classnames";
import Icon, { IconSize, IconType } from "app/common/components/icon/icon";
import "app/common/components/sliding-window/sliding-window.scss";

interface Props {
	title: string;
	isOpen: boolean;
	onClose: () => void;
	children?: React.ReactNode;
}

export default function SlidingWindow(props: Props): ReactElement {
	const { isOpen, title, children, onClose } = props;

	return (
		<div className="sliding-window">
			{isOpen && <div className="sliding-window__underlayer" onClick={onClose} />}

			<div className={cn("sliding-window-wrapper", { "sliding-window-wrapper_open": isOpen })}>
				<button type="button" className="sliding-window-wrapper__close-button" onClick={onClose}>
					<Icon type={IconType.close} size={IconSize.small} />
				</button>

				<div className="sliding-window-wrapper__page">
					<p className="sliding-window-wrapper__title">{title}</p>
					<div className="sliding-window-wrapper__content">{children}</div>
				</div>
			</div>
		</div>
	);
}
