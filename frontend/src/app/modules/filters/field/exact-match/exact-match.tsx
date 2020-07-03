import Icon, { IconType } from 'app/common/components/icon/icon';
import 'app/modules/filters/field/exact-match/exact-match.scss';
import cn from 'classnames';
import React from 'react';

interface Props {
	exactMatch: boolean
	onToggle: () => void
}

class ExactMatch extends React.PureComponent<Props> {

	render() {
		return (
			<div
				className="exact-match"
				onClick={this.props.onToggle}
			>
				<div className={cn('exact-match__toggle', { 'exact-match__toggle_checked': this.props.exactMatch })}>
					<Icon className="exact-match__icon" type={IconType.exactMatch} size={9} />
				</div>
			</div>
		);
	}
}

export default ExactMatch;
