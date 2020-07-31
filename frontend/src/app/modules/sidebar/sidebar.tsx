import Icon, { IconSize, IconType } from 'app/common/components/icon/icon';

import 'app/modules/sidebar/sidebar.scss';
import { deleteUser } from 'app/common/store/auth/actions';
import { activateSettings } from 'app/common/store/settings/actions';
import { activateVirtualAssistant } from 'app/common/store/virtual-assistant/actions';
import { RouterNames } from 'app/common/types/router.types';
import { RootStore } from 'app/common/types/store.types';

import arrowIcon from 'assets/icons/arrow.icon.svg';
import logoFull from 'assets/images/logo-full.svg';
import logo from 'assets/images/logo.svg';

import cn from 'classnames';
import React from 'react';
import { connect, ConnectedProps } from 'react-redux';
import { Link, RouteComponentProps } from 'react-router-dom';
import Tooltip from "app/common/components/tooltip/tooltip";
import { setStatusTrainModelQAMetrics, clearQAMetricsData } from "app/common/store/qa-metrics/actions"; 
import { clearSettingsData } from "app/common/store/settings/thunks";
 
enum SideBarTabs {
	settings = 'Settings',
	virtualAssistant = 'Ask Nostradamus',
}

interface SideBarState{
	isOpen: boolean,
	actionsBlockOpened: boolean,
}

class Sidebar extends React.Component<Props, SideBarState> {

	state = {
		isOpen: false,
		actionsBlockOpened: false,
	};

	settingsRef: React.RefObject<HTMLUListElement> = React.createRef();
	virtualAssistantRef: React.RefObject<HTMLUListElement>  = React.createRef();

	toggleNav = (opened: boolean) => () => {
		this.setState({
			...this.state,
			isOpen: opened,
			actionsBlockOpened: false,
		});
	};

	toggleActionBlock = () => {
		this.setState({
			...this.state,
			actionsBlockOpened: !this.state.actionsBlockOpened,
		});
	};

	activateTab = (dispatchFunction: any) => () => {
		this.closeSlidingWindow();
		dispatchFunction();
	};

	checkSideBarClickTarget = (e: any) => {
		if(!(	(this.settingsRef.current && this.settingsRef.current.contains(e.target)) ||
					(this.virtualAssistantRef.current && this.virtualAssistantRef.current.contains(e.target)))) this.closeSlidingWindow();
	}

	closeSlidingWindow = () => {
		if (this.props.isSettingsOpen) this.props.activateSettings();
		if (this.props.isVirtualAssistantOpen) this.props.activateVirtualAssistant();
	}
	logOut = () => {
		this.props.deleteUser();
		this.props.clearQAMetricsData();
		this.props.clearSettingsData();
	};

	render() {
		const { pathname } = this.props.location;
		
		return (
			<div
				className={cn('navigation-bar', { 'navigation-bar_opened': this.state.isOpen })}
				onMouseEnter={this.toggleNav(true)} onMouseLeave={this.toggleNav(false)}
				onClick = {this.checkSideBarClickTarget}
			>
				<div className="navigation-bar__inner">

					<img
						className={cn('navigation-bar__logo', { 'navigation-bar__logo_hidden': this.state.isOpen })} src={logo}
						alt="Nostradamus Logo"
					/>
					<img
						className={cn('navigation-bar__logo-full', { 'navigation-bar__logo-full_hidden': !this.state.isOpen })}
						src={logoFull} alt="Nostradamus Logo"
					/>

					<div className="navigation-bar__user">
						<div className="navigation-bar__user-photo">
							{this.props.user && this.props.user.name[0].toUpperCase()}
						</div>

						<div className="navigation-bar__user-data">
							<div className="navigation-bar__user-name">
								{this.props.user && this.props.user.name}
								<img
									className="navigation-bar__user-manage-icon"
									onClick={this.toggleActionBlock}
									style={{ transform: this.state.actionsBlockOpened ? 'rotate(180deg)' : 'none' }}
									src={arrowIcon}
									alt="arrow icon"
								/>
							</div>
							<div className="navigation-bar__user-email">{this.props.user && this.props.user.email}</div>
						</div>
					</div>

					{
						this.state.actionsBlockOpened &&
            <div className="navigation-bar__actions">
	            {/*excluded section*/}
							{/*
							 <div className="navigation-bar__actions-item disabled">
							 <Icon
							 type={IconType.account}
							 size={IconSize.normal}
							 className="navigation-bar__actions-item-icon"
							 />
							 Account Management
							 </div> */
							}

                <button
                    onClick={this.logOut}
                    className="navigation-bar__actions-item"
                >
                    <Icon
                        type={IconType.logout}
                        size={IconSize.normal}
                        className="navigation-bar__actions-item-icon"
                    />
                    Log Out
                </button>
            </div>
					}

					<nav className="navigation-bar__menu">
						<ul>
							<Link
								to={RouterNames.analysisAndTraining}
								className={cn('navigation-bar__menu-item', { 'navigation-bar__menu-item_active': pathname === RouterNames.analysisAndTraining })}
							>
								<div className="navigation-bar__menu-item-icon">
									<Icon
										type={IconType.analysis}
										size={IconSize.big}
									/>
								</div>

								<div className="navigation-bar__menu-item-text">
									Analysis & Training
								</div>
							</Link>

								<Link
									to={RouterNames.descriptionAssessment}
									className={cn('navigation-bar__menu-item', 
												{ 'navigation-bar__menu-item_active': pathname === RouterNames.descriptionAssessment })}
								>
									<div className="navigation-bar__menu-item-icon">
											<Icon type={IconType.description}
														size={IconSize.big}/>
									</div>

									<div className="navigation-bar__menu-item-text">
										Description Assessment
									</div>
								</Link>
							
								<Link
									to={RouterNames.qaMetrics}
									className={cn('navigation-bar__menu-item', 
												{ 'navigation-bar__menu-item_active': pathname === RouterNames.qaMetrics })}
								>

									<div className="navigation-bar__menu-item-icon">
										<Icon
											type={IconType.QAMetrics}
											size={IconSize.big}
										/>
									</div>

									<div className="navigation-bar__menu-item-text">
										QA Metrics
									</div>
								</Link>

						</ul>
					</nav>

					<nav className="navigation-bar__menu navigation-bar__menu_position_bottom">
						
						<ul ref={this.virtualAssistantRef}>
								
								<li
									className={cn('navigation-bar__menu-item', 
												  { 'navigation-bar__menu-item_active': this.props.isVirtualAssistantOpen })}
									onClick={this.activateTab(this.props.activateVirtualAssistant)}
								>
									<div className="navigation-bar__menu-item-icon">
										<Icon
											type={IconType.chatBeta}
											size={IconSize.big}
										/>
									</div>

									<div className="navigation-bar__menu-item-text">
										{SideBarTabs.virtualAssistant}
									</div>
								</li>
						</ul>

						<ul ref={this.settingsRef}>
							<Tooltip message="Uploading data. Please wait a few minutes." isDisplayed={!this.props.isCollectingFinished} duration={1}>
								<li
									className={cn('navigation-bar__menu-item', 
												{ 'navigation-bar__menu-item_active': this.props.isSettingsOpen },
												{ 'navigation-bar__menu-item_disabled': !this.props.isCollectingFinished })}
									onClick={this.activateTab(this.props.activateSettings)}
								>
									<div className="navigation-bar__menu-item-icon">
										<Icon
											type={IconType.settings}
											size={IconSize.big}
										/>
									</div>

									<div className="navigation-bar__menu-item-text">
										{SideBarTabs.settings}
									</div>
								</li>
							</Tooltip>
						</ul>

					</nav>
				</div>
			</div>
		);
	}
}

const mapStateToProps = (store: RootStore) => ({
	user: store.auth.user,
	isSettingsOpen: store.settings.settingsStore.isOpen,
	isVirtualAssistantOpen: store.virtualAssistant.isOpen,
	isCollectingFinished: store.settings.settingsStore.isCollectingFinished,
});

const mapDispatchToProps = {
	deleteUser,
	activateSettings,
	activateVirtualAssistant,
	setStatusTrainModelQAMetrics,
	clearQAMetricsData,
	clearSettingsData
};

const connector = connect(
	mapStateToProps,
	mapDispatchToProps,
);

type PropsFromRedux = ConnectedProps<typeof connector>

type Props = PropsFromRedux & RouteComponentProps;

export default connector(Sidebar);
