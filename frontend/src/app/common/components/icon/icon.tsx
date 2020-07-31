import React from 'react';
import cn from 'classnames';

import './icon.scss';

export enum IconType {
	account = 'icon-Account',
	add = 'icon-Add',
	analysis = 'icon-analysis',
	bugTracker = 'icon-Bug-Tracker',
	calendar = 'icon-Calendar',
	check = 'icon-Check',
	close = 'icon-Close',
	delete = 'icon-Delete',
	description = 'icon-Description',
	down = 'icon-Down',
	edit2 = 'icon-Edit2',
	exclam = 'icon-Exclam',
	filter1 = 'icon-Filter-1',
	filter = 'icon-Filter',
	left = 'icon-Left',
	lock = 'icon-Lock',
	login = 'icon-Login',
	logout = 'icon-Logout',
	QAMetrics = 'icon-QA-Metrics',
	register = 'icon-Register',
	remove = 'icon-Remove',
	right = 'icon-Right',
	settings = 'icon-Settings',
	trainModel = 'icon-Train-Model',
	undo = 'icon-Undo',
	upload = 'icon-Upload',
	exactMatch = 'icon-Exact-Match',
	chat = 'icon-chat',
	send = 'icon-Send',
	chatBeta = 'icon-chatbeta',
	file = 'icon-file',
	warning = 'icon-warning',
}

export enum IconSize {
	small = 14,
	normal = 24,
	big = 32,
}

type IconProps = {
	type: IconType,
	size: IconSize | number,
	className?: string
}

class Icon extends React.Component<IconProps> {

	static defaultProps = {
		size: IconSize.normal,
	};

	render() {
		return (
			<span
				className={cn('icon', this.props.type, this.props.className)}
				style={{
					fontSize: this.props.size,
				}}
			>{/* icon */}</span>
		);
	}
}

export default Icon;
