import Button, { ButtonStyled } from "app/common/components/button/button";
import { IconType, IconSize } from "app/common/components/icon/icon";
import "./settings_layout.scss";
import React from "react";

interface SettingsLayoutProps {
	title: string;
	children: React.ReactNode;

	cancelButtonTitle?: string;
	cancelButtonDisable: boolean;
	cancelButtonHandler: () => void;

	saveButtonTitle?: string;
	saveButtonDisable: boolean;
	saveButtonHandler: () => void;
}

export default function SettingsLayout(props: SettingsLayoutProps) {
	return (
		<div className="settings-layout">
			<p className="settings-layout__title">{props.title}</p>
			{props.children}
			<div className="settings-layout__footer">
				<Button
					text={props.cancelButtonTitle || "Cancel"}
					icon={IconType.close}
					iconSize={IconSize.normal}
					styled={ButtonStyled.Flat}
					onClick={props.cancelButtonHandler}
					disabled={props.cancelButtonDisable}
				/>
				<Button
					text={props.saveButtonTitle || "Save Changes"}
					icon={IconType.check}
					iconSize={IconSize.normal}
					onClick={props.saveButtonHandler}
					disabled={props.saveButtonDisable}
				/>
			</div>
		</div>
	);
}
