import pytest
from datetime import date, timedelta
from tests.conftest import TrackingTestDAO

class TestTrackingDAO:

    async def test_create_completion_work_correct(self, db_session, sample_user, sample_habit):
        """TrackingDAO.create_completion(): должен правильно создавать запись о выполнении привычки"""
        result=await TrackingTestDAO.create_completion(session=db_session, user_id=sample_user.id, habit_id=sample_habit.id)
        assert result is not None
        assert result.habit_id==sample_habit.id
        assert result.user_id==sample_user.id
        assert result.completed_date==date.today()
        assert result.current_streak==1
        assert result.longest_streak==1

    async def test_create_completion_continues_streak(self, db_session, sample_user, sample_habit):
        """TrackingDAO.create_completion(): должен правильно продливать серию выполнений"""
        day1=await TrackingTestDAO.create_completion(session=db_session, user_id=sample_user.id, habit_id=sample_habit.id)
        day1.completed_date=date.today()-timedelta(days=1)
        await db_session.flush()
        day2=await TrackingTestDAO.create_completion(session=db_session, user_id=sample_user.id, habit_id=sample_habit.id)
        assert day2.current_streak==2
        assert day2.longest_streak==2
    
    async def test_create_completion_resets_streak(self, db_session, sample_user, sample_habit):
        """TrackingDAO.create_completion(): должен правильно сбрасывать серию при пропуске дня"""
        day1=await TrackingTestDAO.create_completion(session=db_session, user_id=sample_user.id, habit_id=sample_habit.id)
        day1.completed_date=date.today()-timedelta(days=2)
        await db_session.flush()
        day3=await TrackingTestDAO.create_completion(session=db_session, user_id=sample_user.id, habit_id=sample_habit.id)
        assert day3.current_streak==1
        assert day3.longest_streak==1
    
    async def test_create_completion_raises_error_for_duplicate(self, db_session, sample_user, sample_habit):
        """TrackingDAO.create_completion(): должен выдавать ошибку при повторной отметке в тот же день"""
        result=await TrackingTestDAO.create_completion(session=db_session, user_id=sample_user.id, habit_id=sample_habit.id)
        assert result is not None
        with pytest.raises(ValueError, match="Привычка уже отмечена сегодня"):
            await TrackingTestDAO.create_completion(session=db_session, user_id=sample_user.id, habit_id=sample_habit.id)

    
    async def test_get_heatmap_data_returns_dict_with_dates(self, db_session, sample_user, sample_habit):
        """TrackingDAO.get_heatmap_data(): должен правильно возвращать словарь с датами"""
        await TrackingTestDAO.create_completion(session=db_session, user_id=sample_user.id, habit_id=sample_habit.id)
        result=await TrackingTestDAO.get_heatmap_data(session=db_session, habit_id=sample_habit.id, days=30)
        assert isinstance(result, dict)
        assert len(result)==30
        assert all(isinstance(date_str, str) for date_str in result.keys())
        assert all(value in (0,1) for value in result.values())
        today_str=date.today().isoformat()
        assert result[today_str]==1

    async def test_get_heatmap_data_empty_habit(self, db_session, sample_habit):
        """TrackingDAO.get_heatmap_data(): все нули для привычки без выполнений"""
        result=await TrackingTestDAO.get_heatmap_data(session=db_session, habit_id=sample_habit.id, days=30)
        assert all(value==0 for value in result.values())

    async def test_get_heatmap_data_custom_days(self, db_session, sample_habit):
        """TrackingDAO.get_heatmap_data(): должен правильно работать с разным количеством дней"""
        test_days=[30, 90, 365]
        for days in test_days:
            result=await TrackingTestDAO.get_heatmap_data(session=db_session, habit_id=sample_habit.id, days=days)
            assert len(result)==days
    

    async def test_get_heatmap_stats_calculates_correct_stats(self, db_session, sample_habit, sample_user):
        """TrackingDAO.get_heatmap_stats(): должен правильно рассчитывать статистику"""
        day1=await TrackingTestDAO.create_completion(session=db_session, user_id=sample_user.id, habit_id=sample_habit.id)
        day1.completed_date=date.today()-timedelta(days=1)
        await db_session.flush()
        day2=await TrackingTestDAO.create_completion(session=db_session, user_id=sample_user.id, habit_id=sample_habit.id)
        result=await TrackingTestDAO.get_heatmap_stats(session=db_session, habit_id=sample_habit.id, days=30)
        assert result['total_completions']==2
        assert result['completion_rate']==round((2/30)*100, 1)
        assert result['current_streak']==2
        assert result['longest_streak']==2

    async def test_get_heatmap_stats_no_completions(self, db_session, sample_habit):
        """TrackingDAO.get_heatmap_stats(): должен возвращать нули для привычки без выполнений"""
        result=await TrackingTestDAO.get_heatmap_stats(session=db_session, habit_id=sample_habit.id, days=30)
        assert result['total_completions']==0
        assert result['completion_rate']==0
        assert result['current_streak']==0
        assert result['longest_streak']==0






