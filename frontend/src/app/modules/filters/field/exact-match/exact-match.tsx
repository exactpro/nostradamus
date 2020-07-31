import Icon, { IconType } from 'app/common/components/icon/icon';
import 'app/modules/filters/field/exact-match/exact-match.scss';
import cn from 'classnames';
import React from 'react';
import Tooltip from 'app/common/components/tooltip/tooltip';

interface Props {
	exactMatch: boolean
	onToggle: () => void
}

class ExactMatch extends React.PureComponent<Props> {

	render() {
		return (
			<Tooltip duration={1} message="Exact Match">
				<div
					className="exact-match"
					onClick={this.props.onToggle}
				>
					<div className={cn('exact-match__toggle', { 'exact-match__toggle_checked': this.props.exactMatch })}>
						<Icon className="exact-match__icon" type={IconType.exactMatch} size={8} />
					</div>
				</div>
			</Tooltip>
		);
	}
}

export default ExactMatch;
