import 'app/common/components/card/card.scss';
import CircleSpinner from 'app/common/components/circle-spinner/circle-spinner';
import Icon, { IconType } from 'app/common/components/icon/icon';
import { isOneOf } from 'app/common/functions/helper';
import { HttpStatus } from 'app/common/types/http.types';
import cn from 'classnames';
import React from 'react';

// TODO: refactor to meet solid principles (left only view, remove unnecessary logic)
interface CardProps {
	title?: string;
	className?: string;
	previewImage?: string;
	hoverHeader?: boolean; // for the situation, when we have elements in header of card
	warningMessage?: string
	status: HttpStatus;
}

class Card extends React.Component<CardProps> {

	static defaultProps = {
		status: HttpStatus.FINISHED,
	};

	render() {

		const { status } = this.props;
		const S = HttpStatus;

		let whenShowPreviewManage = [S.PREVIEW, S.LOADING, S.WARNING];
		let cardContentStyle: any = {
			backgroundImage: isOneOf(status, whenShowPreviewManage) ? `url(${this.props.previewImage})` : 'none',
		};

		if (status === S.WARNING) {
			cardContentStyle = {
				...cardContentStyle,
				filter: 'blur(3px)'
			};
		}

		return (
			<section className={cn('card', this.props.className)}>
				{
					this.props.title &&
          <h3 className="card__title" style={{ position: this.props.hoverHeader ? 'absolute' : 'static' }}>
						{this.props.title}
          </h3>
				}

				{
					isOneOf(status, [S.LOADING]) &&
          <CircleSpinner alignCenter />
				}

				{
					status === S.WARNING &&
          <div className="card__warning-overlay">
							<Icon type={IconType.warning} className="card__warning-icon" size={48}/>

		          <div className="card__warning-message" >
			          { this.props.warningMessage || '' }
		          </div>
          </div>
				}

				<div className="card__content" style={cardContentStyle}>
					{(status === S.FINISHED) && this.props.children}
				</div>
			</section>
		);
	}
}

export default Card;
